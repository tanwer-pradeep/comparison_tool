"use client";
import { useState } from "react";
import { useRouter } from "next/navigation";

export default function NewRunPage() {
    const router = useRouter();
    const [url, setUrl] = useState("");
    const [loading, setLoading] = useState(false);
    const [refImage, setRefImage] = useState<File | null>(null);

    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault();
        setLoading(true);

        const formData = new FormData();
        formData.append("url", url);
        if (refImage) {
            formData.append("reference_image", refImage);
        }

        // Figma logic later

        try {
            const res = await fetch("/api/v1/runs/", {
                method: "POST",
                body: formData,
            });

            if (!res.ok) throw new Error("Run failed to create");

            const data = await res.json();
            router.push(`/runs/${data.id}`);
        } catch (err) {
            console.error(err);
            alert("Failed to start run");
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="max-w-4xl mx-auto py-10 px-4">
            <h1 className="text-3xl font-bold mb-8">Start Visual Comparison</h1>

            <form onSubmit={handleSubmit} className="space-y-6 bg-card p-6 rounded-lg border shadow-sm">
                <div className="grid gap-2">
                    <label htmlFor="url" className="text-sm font-medium">Dev App URL</label>
                    <input
                        id="url"
                        type="url"
                        required
                        className="flex h-10 w-full rounded-md border border-input bg-background px-3 py-2 text-sm ring-offset-background file:border-0 file:bg-transparent file:text-sm file:font-medium placeholder:text-muted-foreground focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 disabled:cursor-not-allowed disabled:opacity-50"
                        placeholder="http://localhost:3000"
                        value={url}
                        onChange={(e) => setUrl(e.target.value)}
                    />
                </div>

                <div className="grid gap-2">
                    <label htmlFor="refImage" className="text-sm font-medium">Reference Screenshot (Optional)</label>
                    <input
                        id="refImage"
                        type="file"
                        accept="image/*"
                        onChange={(e) => setRefImage(e.target.files?.[0] || null)}
                        className="flex h-10 w-full rounded-md border border-input bg-background px-3 py-2 text-sm"
                    />
                    <p className="text-xs text-muted-foreground">Upload a design mockup or previous screenshot to compare against.</p>
                </div>

                <button
                    type="submit"
                    disabled={loading}
                    className="w-full inline-flex items-center justify-center whitespace-nowrap rounded-md text-sm font-medium ring-offset-background transition-colors focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 disabled:pointer-events-none disabled:opacity-50 bg-primary text-primary-foreground hover:bg-primary/90 h-10 px-4 py-2"
                >
                    {loading ? "Initializing Run..." : "Compare URL vs Reference"}
                </button>
            </form>
        </div>
    );
}
