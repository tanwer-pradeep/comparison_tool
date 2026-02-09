import Link from "next/link";

export default function Home() {
    return (
        <div className="flex flex-col items-center justify-center min-h-screen py-2">
            <h1 className="text-6xl font-bold bg-clip-text text-transparent bg-gradient-to-r from-blue-500 to-teal-400">
                Visual QA
            </h1>
            <p className="mt-3 text-2xl text-muted-foreground p-4">
                Automated Visual Regression & Figma Spec Testing
            </p>

            <div className="flex gap-4 mt-8">
                <Link
                    href="/runs/new"
                    className="px-6 py-3 bg-primary text-primary-foreground rounded-lg hover:opacity-90 transition-opacity font-medium"
                >
                    Start New Run
                </Link>
                <Link
                    href="/runs"
                    className="px-6 py-3 border border-input bg-background hover:bg-accent hover:text-accent-foreground rounded-lg transition-colors font-medium"
                >
                    View History
                </Link>
            </div>
        </div>
    );
}
