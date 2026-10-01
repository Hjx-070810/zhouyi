"use client";

import { motion } from "framer-motion";

export default function DivinationAnimation() {
    return (
        <div className="flex flex-col items-center justify-center py-4 relative overflow-hidden">
            {/* Background Ink Splatters (Static or subtle pulse) */}
            <motion.div
                initial={{ opacity: 0, scale: 0.8 }}
                animate={{ opacity: [0.3, 0.5, 0.3], scale: [0.9, 1, 0.9] }}
                transition={{ duration: 4, repeat: Infinity, ease: "easeInOut" }}
                className="absolute inset-0 pointer-events-none flex items-center justify-center"
            >
                <div className="w-64 h-64 bg-stone-200 rounded-full blur-[60px] opacity-50" />
            </motion.div>

            {/* Rotating Bagua / Tai Chi Symbol */}
            <div className="relative w-24 h-24 md:w-32 md:h-32">
                {/* Outer Ring (Bagua Trigrams - Simplified representation) */}
                <motion.div
                    animate={{ rotate: 360 }}
                    transition={{ duration: 20, repeat: Infinity, ease: "linear" }}
                    className="absolute inset-0 border-2 border-stone-300 rounded-full opacity-60 border-dashed"
                />

                <motion.div
                    animate={{ rotate: -360 }}
                    transition={{ duration: 30, repeat: Infinity, ease: "linear" }}
                    className="absolute inset-4 border border-stone-200 rounded-full opacity-40"
                />

                {/* Center Tai Chi (Yin Yang) - CSS implementation */}
                <motion.div
                    animate={{ rotate: 360 }}
                    transition={{ duration: 8, repeat: Infinity, ease: "linear" }}
                    className="absolute inset-0 m-auto w-16 h-16 md:w-24 md:h-24 rounded-full border-2 border-stone-800 overflow-hidden shadow-lg shadow-stone-200"
                    style={{
                        background: "linear-gradient(to right, #2a2a2a 50%, #f5f5f4 50%)",
                    }}
                >
                    {/* Top Circle (White in Black) */}
                    <div className="absolute top-0 left-1/2 -translate-x-1/2 w-1/2 h-1/2 bg-stone-800 rounded-full flex items-center justify-center">
                        <div className="w-1/4 h-1/4 bg-stone-100 rounded-full" />
                    </div>
                    {/* Bottom Circle (Black in White) */}
                    <div className="absolute bottom-0 left-1/2 -translate-x-1/2 w-1/2 h-1/2 bg-stone-100 rounded-full flex items-center justify-center">
                        <div className="w-1/4 h-1/4 bg-stone-800 rounded-full" />
                    </div>
                </motion.div>
            </div>

            {/* Loading Text */}
            <motion.div
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ delay: 0.5 }}
                className="mt-8 text-center space-y-2"
            >
                <h3 className="text-xl font-serif font-bold text-stone-800 tracking-widest">
                    推演天机
                </h3>
                <p className="text-sm text-stone-500 font-song">
                    观象玩占 · 探赜索隐
                </p>
            </motion.div>
        </div>
    );
}
