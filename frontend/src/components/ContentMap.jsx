import React from 'react';

export default function ContentMap({ items = [] }) {
    return (
        <div className="p-4 mt-8 border rounded shadow">
            <h2 className="text-xl font-bold mb-4">Intelligent Content Map</h2>

            {items.length === 0 ? (
                <p>No map items scheduled yet.</p>
            ) : (
                <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
                    {items.map((item, idx) => (
                        <div key={idx} className="p-3 border bg-gray-50 rounded">
                            <h3 className="font-semibold">{item.target_platform} - {item.content_type}</h3>
                            <p className="text-sm">Priority: {item.priority}</p>
                            <p className="text-sm">Planned for: {new Date(item.proposed_date).toLocaleDateString()}</p>
                            <span className="inline-block mt-2 px-2 py-1 bg-blue-100 text-blue-800 text-xs rounded">
                                {item.status}
                            </span>
                        </div>
                    ))}
                </div>
            )}
        </div>
    );
}
