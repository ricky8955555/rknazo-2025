import ctypes
import random
import sys
from argparse import ArgumentParser
from typing import Any, cast


def encrypt(v: tuple[int, int], k: tuple[int, int, int, int]) -> tuple[int, int]:
    # TEA encrypt
    y = ctypes.c_uint32(v[0])
    z = ctypes.c_uint32(v[1])
    sum = ctypes.c_uint32(0)
    delta = 0x9E3779B9
    n = 32

    while n > 0:
        sum.value += delta
        y.value += (z.value << 4) + k[0] ^ z.value + sum.value ^ (z.value >> 5) + k[1]
        z.value += (y.value << 4) + k[2] ^ y.value + sum.value ^ (y.value >> 5) + k[3]
        n -= 1

    return (y.value, z.value)


def bytes_to_int_blocks(b: bytes, block_size: int) -> list[int]:
    # convert bytes to given size unsigned int blocks.
    assert not block_size % 4, "invalid block size."
    return [
        int.from_bytes(b[i : i + block_size], sys.byteorder) for i in range(0, len(b), block_size)
    ]


def gen_data_h_code(flag: str, seed: Any, key: tuple[int, int, int, int]) -> str:
    # generate data.h code

    def gen_byte_ptr_data_init_code(blocks: list[int] | tuple[int, ...], block_size: int) -> str:
        # initialize data in obfuscated way
        in_bytes = list(
            enumerate(
                byte for block in blocks for byte in block.to_bytes(block_size, sys.byteorder)
            )
        )
        rand.shuffle(in_bytes)  # shuffle the order of assignment
        return " ".join(f"ptr[{idx}] = {hex(byte)};" for idx, byte in in_bytes)

    rand = random.Random(seed)  # stablize compile result

    blocks = bytes_to_int_blocks(flag.encode(), 4)
    if len(blocks) % 2:  # padding
        blocks.append(0)

    encrypted = [
        block
        for i in range(0, len(blocks), 2)
        for block in encrypt((blocks[i], blocks[i + 1]), key)
    ]

    return f"""
#include <stdint.h>

#define FLAG_LENGTH {len(encrypted) * 4}

void getflag(char *flag) {{
    // TEA decrypt
    uint32_t k[4];
    uint32_t *v, *end;
    uint32_t sum, i; /* set up */
    uint32_t delta; /* a key schedule constant */
    uint8_t *ptr;
    v = (uint32_t *)flag;
    ptr = (uint8_t *)k;
    {gen_byte_ptr_data_init_code(key, 4)}
    ptr = (uint8_t *)v;
    {gen_byte_ptr_data_init_code(encrypted, 4)}
    end = v + {len(encrypted)};
    do {{
        sum = 0xC6EF3720;
        delta = 0x9E3779B9;
        for (i = 0; i < 32; i++) {{ /* basic cycle start */
            v[1] -= ((v[0] << 4) + k[2]) ^ (v[0] + sum) ^ ((v[0] >> 5) + k[3]);
            v[0] -= ((v[1] << 4) + k[0]) ^ (v[1] + sum) ^ ((v[1] >> 5) + k[1]);
            sum -= delta;
        }} /* end cycle */
    }} while ((v += 2) < end);
}}
""".strip()


if __name__ == "__main__":
    parser = ArgumentParser()
    parser.add_argument("--flag", required=True)
    parser.add_argument("--key", nargs=4, required=True, type=lambda s: int(s, 0))
    parser.add_argument("--seed", required=True)
    parser.add_argument("--output", "-o", default=None)

    args = parser.parse_args()
    key = cast(tuple[int, int, int, int], tuple(args.key))
    code = gen_data_h_code(args.flag, args.seed, key)

    if args.output is None:
        print(code)
    else:
        with open(args.output, "w") as fp:
            fp.write(code)
