import { useState, useEffect } from 'react';
import { leadsApi } from '../services/api';
import { toast } from 'react-hot-toast';
import { CalendarIcon, UsersIcon, EnvelopeIcon, ChartBarIcon } from '@heroicons/react/24/outline';

export default function Campaigns() {
  const [campaigns, setCampaigns] = useState([]);
  const [loading, setLoading] = useState(true);
  const [isModalOpen, setIsModalOpen] = useState(false);
  const [newCampaign, setNewCampaign] = useState({
    name: '',
    subject: '',
    body_template: '',
    target_leads: []
  });

  useEffect(() => {
    // Simulate campaign data - in real app this would come from API
    const mockCampaigns = [
      {
        id: 1,
        name: 'Q1 Follow-up Campaign',
        subject: 'Checking in about your project needs',
        status: 'active',
        sent_count: 45,
        target_count: 100,
        created_at: new Date('2024-01-15')
      },
      {
        id: 2,
        name: 'New Year Outreach',
        subject: 'Happy New Year! Let\'s make 2024 productive',
        status: 'draft',
        sent_count: 0,
        target_count: 200,
        created_at: new Date('2024-01-01')
      }
    ];
    setCampaigns(mockCampaigns);
    setLoading(false);
  }, []);

  const handleCreateCampaign = async (e) => {
    e.preventDefault();
    // In real app, this would call API
    const campaign = {
      id: Date.now(),
      ...newCampaign,
      status: 'draft',
      sent_count: 0,
      target_count: newCampaign.target_leads.length,
      created_at: new Date()
    };
    setCampaigns([...campaigns, campaign]);
    setNewCampaign({ name: '', subject: '', body_template: '', target_leads: [] });
    setIsModalOpen(false);
    toast.success('Campaign created successfully!');
  };

  if (loading) return <div className="p-8 text-center">Loading campaigns...</div>;

  return (
    <div>
      <div className="sm:flex sm:items-center">
        <div className="sm:flex-auto">
          <h1 className="text-xl font-semibold text-gray-900">Campaigns</h1>
          <p className="mt-2 text-sm text-gray-700">Manage your email campaigns and track their performance.</p>
        </div>
        <div className="mt-4 sm:ml-16 sm:mt-0 sm:flex-none">
          <button
            type="button"
            onClick={() => setIsModalOpen(true)}
            className="block rounded-md bg-indigo-600 px-3 py-2 text-center text-sm font-semibold text-white shadow-sm hover:bg-indigo-500 focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-indigo-600"
          >
            New Campaign
          </button>
        </div>
      </div>

      <div className="mt-8 grid grid-cols-1 gap-4 sm:grid-cols-2 lg:grid-cols-4">
        <div className="bg-white px-4 py-5 shadow rounded-lg overflow-hidden sm:p-6">
          <div className="flex items-center">
            <div className="flex-shrink-0 bg-indigo-500 rounded-md p-3">
              <CalendarIcon className="h-6 w-6 text-white" aria-hidden="true" />
            </div>
            <div className="ml-5 w-0 flex-1">
              <dl>
                <dt className="text-sm font-medium text-gray-500 truncate">Total Campaigns</dt>
                <dd className="text-lg font-medium text-gray-900">{campaigns.length}</dd>
              </dl>
            </div>
          </div>
        </div>
        <div className="bg-white px-4 py-5 shadow rounded-lg overflow-hidden sm:p-6">
          <div className="flex items-center">
            <div className="flex-shrink-0 bg-green-500 rounded-md p-3">
              <EnvelopeIcon className="h-6 w-6 text-white" aria-hidden="true" />
            </div>
            <div className="ml-5 w-0 flex-1">
              <dl>
                <dt className="text-sm font-medium text-gray-500 truncate">Emails Sent</dt>
                <dd className="text-lg font-medium text-gray-900">
                  {campaigns.reduce((sum, c) => sum + c.sent_count, 0)}
                </dd>
              </dl>
            </div>
          </div>
        </div>
        <div className="bg-white px-4 py-5 shadow rounded-lg overflow-hidden sm:p-6">
          <div className="flex items-center">
            <div className="flex-shrink-0 bg-yellow-500 rounded-md p-3">
              <UsersIcon className="h-6 w-6 text-white" aria-hidden="true" />
            </div>
            <div className="ml-5 w-0 flex-1">
              <dl>
                <dt className="text-sm font-medium text-gray-500 truncate">Active Campaigns</dt>
                <dd className="text-lg font-medium text-gray-900">
                  {campaigns.filter(c => c.status === 'active').length}
                </dd>
              </dl>
            </div>
          </div>
        </div>
        <div className="bg-white px-4 py-5 shadow rounded-lg overflow-hidden sm:p-6">
          <div className="flex items-center">
            <div className="flex-shrink-0 bg-purple-500 rounded-md p-3">
              <ChartBarIcon className="h-6 w-6 text-white" aria-hidden="true" />
            </div>
            <div className="ml-5 w-0 flex-1">
              <dl>
                <dt className="text-sm font-medium text-gray-500 truncate">Avg. Open Rate</dt>
                <dd className="text-lg font-medium text-gray-900">68%</dd>
              </dl>
            </div>
          </div>
        </div>
      </div>

      <div className="mt-8">
        <div className="bg-white shadow overflow-hidden sm:rounded-md">
          <ul className="divide-y divide-gray-200">
            {campaigns.map((campaign) => (
              <li key={campaign.id}>
                <div className="px-4 py-4 sm:px-6">
                  <div className="flex items-center justify-between">
                    <div className="flex-1">
                      <div className="flex items-center justify-between">
                        <p className="text-sm font-medium text-indigo-600 truncate">{campaign.name}</p>
                        <span className={`ml-2 inline-flex rounded-full px-2 text-xs font-semibold leading-5 ${
                          campaign.status === 'active' ? 'bg-green-100 text-green-800' : 'bg-gray-100 text-gray-800'
                        }`}>
                          {campaign.status}
                        </span>
                      </div>
                      <div className="mt-2 sm:flex sm:justify-between">
                        <div className="sm:flex">
                          <p className="flex items-center text-sm text-gray-500">
                            Subject: {campaign.subject}
                          </p>
                        </div>
                        <div className="mt-2 flex items-center text-sm text-gray-500 sm:mt-0">
                          <p>
                            {campaign.sent_count} / {campaign.target_count} sent
                          </p>
                        </div>
                      </div>
                    </div>
                  </div>
                </div>
              </li>
            ))}
          </ul>
        </div>
      </div>

      {/* Create Campaign Modal */}
      {isModalOpen && (
        <div className="fixed z-10 inset-0 overflow-y-auto">
          <div className="flex items-end justify-center min-h-screen pt-4 px-4 pb-20 text-center sm:block sm:p-0">
            <div className="fixed inset-0 bg-gray-500 bg-opacity-75 transition-opacity" onClick={() => setIsModalOpen(false)}></div>
            <div className="inline-block align-bottom bg-white rounded-lg text-left overflow-hidden shadow-xl transform transition-all sm:my-8 sm:align-middle sm:max-w-lg sm:w-full">
              <form onSubmit={handleCreateCampaign}>
                <div className="bg-white px-4 pt-5 pb-4 sm:p-6 sm:pb-4">
                  <div className="mb-4">
                    <label className="block text-sm font-medium text-gray-700">Campaign Name</label>
                    <input
                      type="text"
                      required
                      value={newCampaign.name}
                      onChange={(e) => setNewCampaign({...newCampaign, name: e.target.value})}
                      className="mt-1 block w-full border-gray-300 rounded-md shadow-sm focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm"
                    />
                  </div>
                  <div className="mb-4">
                    <label className="block text-sm font-medium text-gray-700">Subject</label>
                    <input
                      type="text"
                      required
                      value={newCampaign.subject}
                      onChange={(e) => setNewCampaign({...newCampaign, subject: e.target.value})}
                      className="mt-1 block w-full border-gray-300 rounded-md shadow-sm focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm"
                    />
                  </div>
                  <div className="mb-4">
                    <label className="block text-sm font-medium text-gray-700">Email Template</label>
                    <textarea
                      required
                      rows={4}
                      value={newCampaign.body_template}
                      onChange={(e) => setNewCampaign({...newCampaign, body_template: e.target.value})}
                      className="mt-1 block w-full border-gray-300 rounded-md shadow-sm focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm"
                    />
                  </div>
                </div>
                <div className="bg-gray-50 px-4 py-3 sm:px-6 sm:flex sm:flex-row-reverse">
                  <button
                    type="submit"
                    className="w-full inline-flex justify-center rounded-md border border-transparent shadow-sm px-4 py-2 bg-indigo-600 text-base font-medium text-white hover:bg-indigo-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500 sm:ml-3 sm:w-auto sm:text-sm"
                  >
                    Create Campaign
                  </button>
                  <button
                    type="button"
                    className="mt-3 w-full inline-flex justify-center rounded-md border border-gray-300 shadow-sm px-4 py-2 bg-white text-base font-medium text-gray-700 hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500 sm:mt-0 sm:ml-3 sm:w-auto sm:text-sm"
                    onClick={() => setIsModalOpen(false)}
                  >
                    Cancel
                  </button>
                </div>
              </form>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}