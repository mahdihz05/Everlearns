import React, { useState } from 'react';

export default function Brainstorming({ workspaceId }) {
    const [topic, setTopic] = useState('');
    const [suggestions, setSuggestions] = useState([]);

    const fetchSuggestions = async () => {
        // Mock API call to backend
        setSuggestions([
            { topic: 'Deep dive into AI in Education', reason: 'Core theme' },
            { topic: 'Top 5 Machine Learning trends', reason: 'Current trend' }
        ]);
    };

    return (
        <div className="p-4 border rounded shadow">
            <h2 className="text-xl font-bold mb-4">Smart Brainstorming</h2>
            <div className="mb-4">
                <button
                    onClick={fetchSuggestions}
                    className="bg-blue-500 text-white px-4 py-2 rounded"
                >
                    Get Topic Suggestions
                </button>
            </div>
            {suggestions.length > 0 && (
                <ul className="list-disc pl-5">
                    {suggestions.map((s, idx) => (
                        <li key={idx}>
                            <strong>{s.topic}</strong> - <span className="text-gray-600">{s.reason}</span>
                        </li>
                    ))}
                </ul>
            )}
        </div>
    );
}
