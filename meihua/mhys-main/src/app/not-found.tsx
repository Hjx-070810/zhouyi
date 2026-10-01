import Link from "next/link";

export default function NotFound() {
    return (
        <div className="min-h-screen flex flex-col items-center justify-center p-4 text-center">
            <h2 className="text-4xl md:text-6xl font-song font-bold text-stone-800 mb-4">
                迷失
            </h2>
            <p className="text-stone-500 font-serif mb-8 text-lg">
                此处空无一物，唯有虚空。
            </p>
            <Link
                href="/"
                className="px-8 py-3 bg-stone-800 text-white rounded-full hover:bg-stone-700 transition-colors font-serif"
            >
                返回正道
            </Link>
        </div>
    );
}
