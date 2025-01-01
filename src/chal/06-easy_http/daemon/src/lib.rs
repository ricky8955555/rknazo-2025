use litcrypt::{lc, use_litcrypt};
use once_cell::sync::Lazy;

use_litcrypt!();

pub static KEY: Lazy<String> = Lazy::new(|| lc!("th1s_is_@_k3y"));
pub static FLAG: Lazy<String> = Lazy::new(|| lc!("flag{th1s_is_@_f1ag}"));
