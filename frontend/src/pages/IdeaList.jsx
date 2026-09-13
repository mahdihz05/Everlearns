import React, { useState } from 'react';
import Brainstorming from '../components/Brainstorming';
import ContentMap from '../components/ContentMap';

export default function IdeaList() {
    const [mapItems, setMapItems] = useState([]);

    const generateMap = () => {
        // Mock generation of map items from ideas
        const mockItems = [
            { target_platform: 'Twitter', content_type: 'Thread', priority: 1, proposed_date: new Date(), status: 'planned' },
            { target_platform: 'LinkedIn', content_type: 'Post', priority: 2, proposed_date: new Date(Date.now() + 86400000), status: 'planned' },
        ];
        setMapItems(mockItems);
    };

    return (
        <div className="container mx-auto p-4">
            <h1 className="text-3xl font-bold mb-8">Content App V2 Dashboard</h1>

            <Brainstorming workspaceId={1} />

            <div className="mt-8">
                <button
                    onClick={generateMap}
                    className="bg-green-500 text-white px-4 py-2 rounded"
                >
                    Generate Content Map from Ideas
                </button>
            </div>

            <ContentMap items={mapItems} />
        </div>
    );
}
