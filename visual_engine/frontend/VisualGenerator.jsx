import React, { useState } from 'react';

// Mock API call function - in a real application this would connect to the VisualEngineService via a REST/GraphQL API
const mockGenerateVisual = async (requestData) => {
    return new Promise((resolve, reject) => {
        setTimeout(() => {
            if (requestData.prompt) {
                resolve({
                    status: 'success',
                    media_url: `https://mock-provider.local/generated/${requestData.workspace_id}/image.png`,
                    metadata: { aspect_ratio_used: requestData.aspect_ratio || '1:1' }
                });
            } else {
                reject(new Error("Prompt is required"));
            }
        }, 1500);
    });
};

export const VisualGenerator = ({ workspaceId, defaultPlatform = 'GENERIC' }) => {
    const [prompt, setPrompt] = useState('');
    const [visualType, setVisualType] = useState('simple_image');
    const [platform, setPlatform] = useState(defaultPlatform);
    const [status, setStatus] = useState('idle'); // idle, generating, success, error
    const [result, setResult] = useState(null);
    const [error, setError] = useState('');

    const handleGenerate = async () => {
        setStatus('generating');
        setError('');
        setResult(null);

        const requestData = {
            workspace_id: workspaceId,
            prompt,
            visual_type: visualType,
            platform,
        };

        try {
            const res = await mockGenerateVisual(requestData);
            setResult(res);
            setStatus('success');
        } catch (err) {
            setError(err.message || 'Generation failed');
            setStatus('error');
        }
    };

    return (
        <div className="visual-generator p-4 border rounded shadow-sm bg-white">
            <h3 className="text-lg font-bold mb-4">Generate Visual Content</h3>

            <div className="mb-3">
                <label className="block text-sm font-medium mb-1">Visual Type</label>
                <select
                    className="w-full border rounded p-2"
                    value={visualType}
                    onChange={e => setVisualType(e.target.value)}
                >
                    <option value="simple_image">Simple Image</option>
                    <option value="poster">Poster</option>
                    <option value="content_cover">Content Cover</option>
                    <option value="educational">Educational</option>
                    <option value="news">News</option>
                    <option value="advertisement">Advertisement</option>
                    <option value="text_containing">Text Containing</option>
                </select>
            </div>

            <div className="mb-3">
                <label className="block text-sm font-medium mb-1">Platform Preset</label>
                <select
                    className="w-full border rounded p-2"
                    value={platform}
                    onChange={e => setPlatform(e.target.value)}
                >
                    <option value="GENERIC">Generic</option>
                    <option value="TELEGRAM">Telegram</option>
                    <option value="LINKEDIN">LinkedIn</option>
                    <option value="WORDPRESS">WordPress</option>
                </select>
            </div>

            <div className="mb-4">
                <label className="block text-sm font-medium mb-1">Core Concept / Prompt</label>
                <textarea
                    className="w-full border rounded p-2"
                    rows="3"
                    value={prompt}
                    onChange={e => setPrompt(e.target.value)}
                    placeholder="Describe what you want to generate..."
                ></textarea>
            </div>

            <button
                className="bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700 disabled:opacity-50"
                onClick={handleGenerate}
                disabled={status === 'generating' || !prompt.trim()}
            >
                {status === 'generating' ? 'Generating...' : 'Generate Visual'}
            </button>

            {status === 'error' && (
                <div className="mt-4 p-3 bg-red-100 text-red-700 rounded">
                    Error: {error}
                </div>
            )}

            {status === 'success' && result && (
                <div className="mt-6 border-t pt-4">
                    <h4 className="font-semibold mb-2">Generation Result</h4>
                    <div className="bg-gray-100 p-4 rounded flex flex-col items-center">
                        {/* Fake image display for the mock URL */}
                        <div className="w-full max-w-sm aspect-video bg-gray-300 flex items-center justify-center text-gray-500 mb-3 border">
                            [Image placeholder: {result.media_url}]
                        </div>
                        <p className="text-sm text-gray-600 text-center">
                            Media URL: <a href={result.media_url} className="text-blue-500 hover:underline">{result.media_url}</a>
                        </p>
                        {result.metadata && (
                            <p className="text-xs text-gray-500 mt-2">
                                Aspect Ratio: {result.metadata.aspect_ratio_used}
                            </p>
                        )}
                    </div>
                </div>
            )}
        </div>
    );
};

export default VisualGenerator;
