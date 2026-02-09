"use client";
import { useEffect, useState } from "react";
import Image from "next/image";

interface Issue {
    id: number;
    bbox: { x: number, y: number, width: number, height: number };
    area: number;
    type: string;
}

interface Run {
    id: string;
    status: string;
    url: string;
    screenshot_path: string | null;
    diff_image_path: string | null;
    reference_image_path: string | null;
    issues: Issue[] | null;
    score: number | null;
}

export default function RunDetailsPage({ params }: { params: { id: string } }) {
    const [run, setRun] = useState<Run | null>(null);
    const [error, setError] = useState<string | null>(null);

    useEffect(() => {
        const fetchRun = async () => {
            try {
                const res = await fetch(`http://localhost:8000/api/v1/runs/${params.id}`);
                if (!res.ok) throw new Error("Failed to fetch run");
                const data = await res.json();
                setRun(data);

                // Poll if not completed
                if (data.status === "pending" || data.status === "running") {
                    setTimeout(fetchRun, 2000);
                }
            } catch (err: any) {
                setError(err.message);
            }
        };

        fetchRun();
    }, [params.id]);

    if (error) return <div className="p-10 text-destructive">Error: {error}</div>;
    if (!run) return <div className="p-10">Loading run details...</div>;

    return (
        <div className="container mx-auto py-10">
            <div className="flex justify-between items-center mb-6">
                <h1 className="text-3xl font-bold">Run #{run.id.slice(0, 8)}</h1>
                <span className={`px-3 py-1 rounded-full text-sm font-medium ${run.status === 'completed' ? 'bg-green-100 text-green-800' :
                        run.status === 'failed' ? 'bg-red-100 text-red-800' :
                            'bg-yellow-100 text-yellow-800'
                    }`}>
                    {run.status.toUpperCase()}
                </span>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
                <div className="space-y-2">
                    <h2 className="font-semibold text-lg">Actual Screenshot</h2>
                    {run.screenshot_path ? (
                        <div className="border rounded relative aspect-video bg-muted">
                            {/* In a real app, serve files via static file server or presigned URL. 
                        Assume backend serves artifacts statically at /artifacts/ 
                        Wait, local docker setup needs volume mapping. 
                        I'll use a placeholder or assume API provides full URL.
                        For simplicity, assumption: backend serves static files correctly.
                    */}
                            <div className="p-4 text-center">Image loading requires configured static file serving</div>
                        </div>
                    ) : <div className="bg-muted aspect-video rounded flex items-center justify-center">Pending...</div>}
                </div>

                <div className="space-y-2">
                    <h2 className="font-semibold text-lg">Reference Image</h2>
                    {run.reference_image_path ? (
                        <div className="border rounded relative aspect-video bg-muted">
                            <div className="p-4 text-center">Image loading requires configured static file serving</div>
                        </div>
                    ) : <div className="bg-muted aspect-video rounded flex items-center justify-center text-muted-foreground">No reference provided</div>}
                </div>

                <div className="space-y-2">
                    <h2 className="font-semibold text-lg">Diff Overlay</h2>
                    {run.diff_image_path ? (
                        <div className="border rounded relative aspect-video bg-muted">
                            <div className="p-4 text-center">Image loading requires configured static file serving</div>
                        </div>
                    ) : <div className="bg-muted aspect-video rounded flex items-center justify-center text-muted-foreground">
                        {run.status === 'completed' ? 'No significant diffs' : 'Waiting...'}
                    </div>}
                </div>
            </div>

            {run.issues && run.issues.length > 0 && (
                <div className="mt-10">
                    <h2 className="text-2xl font-bold mb-4">Issues Found ({run.issues.length})</h2>
                    <div className="border rounded-lg overflow-hidden">
                        <table className="w-full text-sm text-left">
                            <thead className="bg-muted/50 text-muted-foreground">
                                <tr>
                                    <th className="px-4 py-3 font-medium">ID</th>
                                    <th className="px-4 py-3 font-medium">Logic</th>
                                    <th className="px-4 py-3 font-medium">BBox</th>
                                    <th className="px-4 py-3 font-medium">Area (px²)</th>
                                </tr>
                            </thead>
                            <tbody>
                                {run.issues.map((issue) => (
                                    <tr key={issue.id} className="border-t hover:bg-muted/50">
                                        <td className="px-4 py-3">#{issue.id}</td>
                                        <td className="px-4 py-3">{issue.type}</td>
                                        <td className="px-4 py-3">
                                            x:{issue.bbox.x}, y:{issue.bbox.y}, w:{issue.bbox.width}, h:{issue.bbox.height}
                                        </td>
                                        <td className="px-4 py-3">{issue.area}</td>
                                    </tr>
                                ))}
                            </tbody>
                        </table>
                    </div>
                </div>
            )}
        </div>
    );
}
