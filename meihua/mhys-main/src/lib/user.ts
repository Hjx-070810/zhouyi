import Cookies from 'js-cookie';

const USER_ID_COOKIE = 'meihua_user_id';
const COOKIE_EXPIRES = 365; // 1 year

/**
 * 获取当前用户的匿名 ID
 * 如果不存在则生成新的 UUID
 */
export function getUserId(): string {
    if (typeof window === 'undefined') {
        return '';
    }

    let userId = Cookies.get(USER_ID_COOKIE);

    if (!userId) {
        userId = generateUUID();
        Cookies.set(USER_ID_COOKIE, userId, { expires: COOKIE_EXPIRES });
    }

    return userId;
}

/**
 * 生成 UUID v4
 * 使用简单实现避免额外依赖
 */
function generateUUID(): string {
    // 简单的 UUID 生成，不依赖外部库
    return 'xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx'.replace(/[xy]/g, function (c) {
        const r = Math.random() * 16 | 0;
        const v = c === 'x' ? r : (r & 0x3 | 0x8);
        return v.toString(16);
    });
}

/**
 * 检查用户 ID 是否存在
 */
export function hasUserId(): boolean {
    if (typeof window === 'undefined') {
        return false;
    }
    return !!Cookies.get(USER_ID_COOKIE);
}

/**
 * 清除用户 ID（用于测试/调试）
 */
export function clearUserId(): void {
    if (typeof window === 'undefined') {
        return;
    }
    Cookies.remove(USER_ID_COOKIE);
}
