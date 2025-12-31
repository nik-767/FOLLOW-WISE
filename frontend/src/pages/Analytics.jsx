import { useState, useEffect } from 'react';
import { leadsApi, emailsApi } from '../services/api';
import { 
  ChartBarIcon, 
  UsersIcon, 
  EnvelopeIcon,
  CalendarIcon,
  ArrowTrendingUpIcon,
  ArrowTrendingDownIcon
} from '@heroicons/react/24/outline';

export default function Analytics() {
  const [analytics, setAnalytics] = useState({
    totalLeads: 0,
    totalEmails: 0,
    openRate: 0,
    replyRate: 0,
    conversionRate: 0,
    monthlyData: [],
    leadStatusBreakdown: []
  });
  const [loading, setLoading] = useState(true);
  const [timeRange, setTimeRange] = useState('30d');

  useEffect(() => {
    fetchAnalytics();
  }, [timeRange]);

  const fetchAnalytics = async () => {
    try {
      // Simulate analytics data - in real app this would come from API
      const mockAnalytics = {
        totalLeads: 156,
        totalEmails: 342,
        openRate: 68.5,
        replyRate: 24.3,
        conversionRate: 12.8,
        monthlyData: [
          { month: 'Jan', leads: 45, emails: 89, conversions: 8 },
          { month: 'Feb', leads: 52, emails: 102, conversions: 11 },
          { month: 'Mar', leads: 59, emails: 151, conversions: 13 }
        ],
        leadStatusBreakdown: [
          { status: 'new', count: 45, percentage: 28.8 },
          { status: 'in_progress', count: 67, percentage: 42.9 },
          { status: 'won', count: 28, percentage: 17.9 },
          { status: 'lost', count: 16, percentage: 10.3 }
        ]
      };
      setAnalytics(mockAnalytics);
    } catch (error) {
      console.error('Failed to fetch analytics:', error);
    } finally {
      setLoading(false);
    }
  };

  if (loading) return <div className="p-8 text-center">Loading analytics...</div>;

  return (
    <div>
      <div className="sm:flex sm:items-center">
        <div className="sm:flex-auto">
          <h1 className="text-xl font-semibold text-gray-900">Analytics</h1>
          <p className="mt-2 text-sm text-gray-700">Track your sales performance and email campaign metrics.</p>
        </div>
        <div className="mt-4 sm:ml-16 sm:mt-0 sm:flex-none">
          <select
            value={timeRange}
            onChange={(e) => setTimeRange(e.target.value)}
            className="block rounded-md border-gray-300 shadow-sm focus:border-indigo-500 focus:ring-indigo-500 sm:text-sm"
          >
            <option value="7d">Last 7 days</option>
            <option value="30d">Last 30 days</option>
            <option value="90d">Last 90 days</option>
            <option value="1y">Last year</option>
          </select>
        </div>
      </div>

      {/* Key Metrics */}
      <div className="mt-8 grid grid-cols-1 gap-4 sm:grid-cols-2 lg:grid-cols-5">
        <div className="bg-white px-4 py-5 shadow rounded-lg overflow-hidden sm:p-6">
          <div className="flex items-center">
            <div className="flex-shrink-0 bg-blue-500 rounded-md p-3">
              <UsersIcon className="h-6 w-6 text-white" aria-hidden="true" />
            </div>
            <div className="ml-5 w-0 flex-1">
              <dl>
                <dt className="text-sm font-medium text-gray-500 truncate">Total Leads</dt>
                <dd className="text-lg font-medium text-gray-900">{analytics.totalLeads}</dd>
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
                <dd className="text-lg font-medium text-gray-900">{analytics.totalEmails}</dd>
              </dl>
            </div>
          </div>
        </div>
        <div className="bg-white px-4 py-5 shadow rounded-lg overflow-hidden sm:p-6">
          <div className="flex items-center">
            <div className="flex-shrink-0 bg-yellow-500 rounded-md p-3">
              <ChartBarIcon className="h-6 w-6 text-white" aria-hidden="true" />
            </div>
            <div className="ml-5 w-0 flex-1">
              <dl>
                <dt className="text-sm font-medium text-gray-500 truncate">Open Rate</dt>
                <dd className="text-lg font-medium text-gray-900">{analytics.openRate}%</dd>
              </dl>
            </div>
          </div>
        </div>
        <div className="bg-white px-4 py-5 shadow rounded-lg overflow-hidden sm:p-6">
          <div className="flex items-center">
            <div className="flex-shrink-0 bg-purple-500 rounded-md p-3">
              <ArrowTrendingUpIcon className="h-6 w-6 text-white" aria-hidden="true" />
            </div>
            <div className="ml-5 w-0 flex-1">
              <dl>
                <dt className="text-sm font-medium text-gray-500 truncate">Reply Rate</dt>
                <dd className="text-lg font-medium text-gray-900">{analytics.replyRate}%</dd>
              </dl>
            </div>
          </div>
        </div>
        <div className="bg-white px-4 py-5 shadow rounded-lg overflow-hidden sm:p-6">
          <div className="flex items-center">
            <div className="flex-shrink-0 bg-indigo-500 rounded-md p-3">
              <ArrowTrendingUpIcon className="h-6 w-6 text-white" aria-hidden="true" />
            </div>
            <div className="ml-5 w-0 flex-1">
              <dl>
                <dt className="text-sm font-medium text-gray-500 truncate">Conversion Rate</dt>
                <dd className="text-lg font-medium text-gray-900">{analytics.conversionRate}%</dd>
              </dl>
            </div>
          </div>
        </div>
      </div>

      {/* Charts Section */}
      <div className="mt-8 grid grid-cols-1 gap-8 lg:grid-cols-2">
        {/* Monthly Trend */}
        <div className="bg-white shadow rounded-lg">
          <div className="px-4 py-5 sm:p-6">
            <h3 className="text-lg leading-6 font-medium text-gray-900">Monthly Performance</h3>
            <div className="mt-5">
              <div className="space-y-4">
                {analytics.monthlyData.map((month, index) => (
                  <div key={month.month} className="flex items-center">
                    <div className="w-12 text-sm font-medium text-gray-900">{month.month}</div>
                    <div className="flex-1 mx-4">
                      <div className="flex items-center space-x-2">
                        <div className="flex-1 bg-gray-200 rounded-full h-2">
                          <div 
                            className="bg-blue-600 h-2 rounded-full" 
                            style={{ width: `${(month.leads / Math.max(...analytics.monthlyData.map(d => d.leads))) * 100}%` }}
                          ></div>
                        </div>
                        <span className="text-xs text-gray-600 w-8">{month.leads}</span>
                      </div>
                      <div className="flex items-center space-x-2 mt-1">
                        <div className="flex-1 bg-gray-200 rounded-full h-2">
                          <div 
                            className="bg-green-600 h-2 rounded-full" 
                            style={{ width: `${(month.emails / Math.max(...analytics.monthlyData.map(d => d.emails))) * 100}%` }}
                          ></div>
                        </div>
                        <span className="text-xs text-gray-600 w-8">{month.emails}</span>
                      </div>
                    </div>
                    <div className="text-sm font-medium text-indigo-600">{month.conversions} conv</div>
                  </div>
                ))}
              </div>
              <div className="mt-4 flex items-center space-x-6 text-xs text-gray-500">
                <div className="flex items-center">
                  <div className="w-3 h-3 bg-blue-600 rounded-full mr-2"></div>
                  <span>Leads</span>
                </div>
                <div className="flex items-center">
                  <div className="w-3 h-3 bg-green-600 rounded-full mr-2"></div>
                  <span>Emails</span>
                </div>
              </div>
            </div>
          </div>
        </div>

        {/* Lead Status Breakdown */}
        <div className="bg-white shadow rounded-lg">
          <div className="px-4 py-5 sm:p-6">
            <h3 className="text-lg leading-6 font-medium text-gray-900">Lead Status Breakdown</h3>
            <div className="mt-5">
              <div className="space-y-3">
                {analytics.leadStatusBreakdown.map((status) => (
                  <div key={status.status} className="flex items-center justify-between">
                    <div className="flex items-center">
                      <div className={`w-3 h-3 rounded-full mr-3 ${
                        status.status === 'new' ? 'bg-blue-500' :
                        status.status === 'in_progress' ? 'bg-yellow-500' :
                        status.status === 'won' ? 'bg-green-500' : 'bg-red-500'
                      }`}></div>
                      <span className="text-sm font-medium text-gray-900 capitalize">{status.status.replace('_', ' ')}</span>
                    </div>
                    <div className="flex items-center space-x-4">
                      <div className="w-24 bg-gray-200 rounded-full h-2">
                        <div 
                          className={`h-2 rounded-full ${
                            status.status === 'new' ? 'bg-blue-500' :
                            status.status === 'in_progress' ? 'bg-yellow-500' :
                            status.status === 'won' ? 'bg-green-500' : 'bg-red-500'
                          }`}
                          style={{ width: `${status.percentage}%` }}
                        ></div>
                      </div>
                      <span className="text-sm text-gray-600 w-12 text-right">{status.count}</span>
                      <span className="text-xs text-gray-500 w-10 text-right">{status.percentage}%</span>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* Performance Insights */}
      <div className="mt-8 bg-white shadow rounded-lg">
        <div className="px-4 py-5 sm:p-6">
          <h3 className="text-lg leading-6 font-medium text-gray-900">Performance Insights</h3>
          <div className="mt-5 grid grid-cols-1 gap-4 sm:grid-cols-2 lg:grid-cols-3">
            <div className="border-l-4 border-green-500 bg-green-50 p-4">
              <div className="flex">
                <div className="flex-shrink-0">
                  <ArrowTrendingUpIcon className="h-5 w-5 text-green-400" aria-hidden="true" />
                </div>
                <div className="ml-3">
                  <p className="text-sm text-green-700">
                    <span className="font-medium">Great job!</span> Your open rate is {analytics.openRate}%, which is above the industry average of 45%.
                  </p>
                </div>
              </div>
            </div>
            <div className="border-l-4 border-yellow-500 bg-yellow-50 p-4">
              <div className="flex">
                <div className="flex-shrink-0">
                  <CalendarIcon className="h-5 w-5 text-yellow-400" aria-hidden="true" />
                </div>
                <div className="ml-3">
                  <p className="text-sm text-yellow-700">
                    <span className="font-medium">Follow-up timing:</span> Leads responded to within 24 hours have a 35% higher conversion rate.
                  </p>
                </div>
              </div>
            </div>
            <div className="border-l-4 border-blue-500 bg-blue-50 p-4">
              <div className="flex">
                <div className="flex-shrink-0">
                  <UsersIcon className="h-5 w-5 text-blue-400" aria-hidden="true" />
                </div>
                <div className="ml-3">
                  <p className="text-sm text-blue-700">
                    <span className="font-medium">Top performing:</span> Leads from "in_progress" status have the highest engagement.
                  </p>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}