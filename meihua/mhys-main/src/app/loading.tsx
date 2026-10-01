import { Loader2 } from "lucide-react";

export default function Loading() {
    return (
        <div className="min-h-screen flex items-center justify-center">
            <div className="flex flex-col items-center gap-4 text-stone-500">
                <Loader2 className="w-8 h-8 animate-spin" />
                <p className="font-serif tracking-widest">推演中...</p>
            </div>
        </div>
    );
}
