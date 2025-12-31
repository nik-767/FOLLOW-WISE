import { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { leadsApi } from '../services/api';
import { toast } from 'react-hot-toast';
import { 
  EnvelopeIcon, 
  SparklesIcon, 
  ClipboardDocumentIcon, 
  PaperAirplaneIcon 
} from '@heroicons/react/24/outline';

export default function LeadDetail() {
  const { id } = useParams();
  const navigate = useNavigate();
  const [lead, setLead] = useState(null);
  const [loading, setLoading] = useState(true);
  
  // AI State
  const [generating, setGenerating] = useState(false);
  const [suggestions, setSuggestions] = useState([]);
  const [tone, setTone] = useState('polite');
  const [sending, setSending] = useState(null); // stores ID of suggestion being sent

  useEffect(() => {
    fetchLeadAndSuggestions();
  }, [id]);

  const fetchLeadAndSuggestions = async () => {
    try {
      const leadRes = await leadsApi.getLead(id);
      setLead(leadRes.data);
      
      // Also fetch existing suggestions if any
      const suggRes = await leadsApi.getFollowups(id);
      setSuggestions(suggRes.data);
    } catch (error) {
      console.error('Error:', error);
      toast.error('Could not load lead details');
    } finally {
      setLoading(false);
    }
  };

  const handleGenerate = async () => {
    setGenerating(true);
    try {
      const response = await leadsApi.generateFollowups(id, { tone });
      setSuggestions(response.data.suggestions);
      toast.success('AI suggestions generated!');
    } catch (error) {
      toast.error('Failed to generate suggestions');
    } finally {
      setGenerating(false);
    }
  };

  const handleSend = async (suggestion) => {
    setSending(suggestion.variant_index);
    try {
      await leadsApi.sendEmail(id, {
        to_email: lead.contact_email,
        subject: suggestion.subject,
        body: suggestion.body,
        provider: 'gmail'
      });
      toast.success('Email sent successfully!');
      // Optional: Refresh lead to show updated status if you implement that
    } catch (error) {
      toast.error('Failed to send email');
    } finally {
      setSending(null);
    }
  };

  const copyToClipboard = (text) => {
    navigator.clipboard.writeText(text);
    toast.success('Copied to clipboard');
  };

  if (loading) return <div className="p-8 text-center">Loading...</div>;
  if (!lead) return <div className="p-8 text-center">Lead not found</div>;

  return (
    <div className="space-y-6">
      {/* Lead Header Card */}
      <div className="bg-white shadow px-4 py-5 sm:rounded-lg sm:p-6">
        <div className="md:flex md:items-center md:justify-between">
          <div className="flex-1 min-w-0">
            <h2 className="text-2xl font-bold leading-7 text-gray-900 sm:text-3xl sm:truncate">
              {lead.contact_name}
            </h2>
            <div className="mt-1 flex flex-col sm:flex-row sm:flex-wrap sm:mt-0 sm:space-x-6">
              <div className="mt-2 flex items-center text-sm text-gray-500">
                <EnvelopeIcon className="flex-shrink-0 mr-1.5 h-5 w-5 text-gray-400" />
                {lead.contact_email}
              </div>
              <div className="mt-2 flex items-center text-sm text-gray-500">
                <span className={`inline-flex rounded-full px-2 text-xs font-semibold leading-5 ${
                   lead.status === 'new' ? 'bg-green-100 text-green-800' : 'bg-gray-100 text-gray-800'
                }`}>
                  {lead.status}
                </span>
              </div>
            </div>
          </div>
        </div>
        <div className="mt-4 border-t border-gray-200 pt-4">
          <dl className="grid grid-cols-1 gap-x-4 gap-y-8 sm:grid-cols-2">
            <div className="sm:col-span-1">
              <dt className="text-sm font-medium text-gray-500">Company</dt>
              <dd className="mt-1 text-sm text-gray-900">{lead.company}</dd>
            </div>
            <div className="sm:col-span-1">
              <dt className="text-sm font-medium text-gray-500">Last Interaction</dt>
              <dd className="mt-1 text-sm text-gray-900">{lead.last_email_snippet || 'None'}</dd>
            </div>
            <div className="sm:col-span-2">
              <dt className="text-sm font-medium text-gray-500">Notes</dt>
              <dd className="mt-1 text-sm text-gray-900">{lead.notes || 'No notes available.'}</dd>
            </div>
          </dl>
        </div>
      </div>

      {/* AI Generator Section */}
      <div className="bg-white shadow sm:rounded-lg">
        <div className="px-4 py-5 sm:p-6">
          <h3 className="text-lg leading-6 font-medium text-gray-900 flex items-center">
            <SparklesIcon className="h-5 w-5 text-purple-500 mr-2" />
            AI Follow-Up Suggestions
          </h3>
          
          <div className="mt-4 flex items-center space-x-4">
            <select
              value={tone}
              onChange={(e) => setTone(e.target.value)}
              className="mt-1 block w-48 pl-3 pr-10 py-2 text-base border-gray-300 focus:outline-none focus:ring-blue-500 focus:border-blue-500 sm:text-sm rounded-md"
            >
              <option value="polite">Polite</option>
              <option value="assertive">Assertive</option>
              <option value="friendly">Friendly</option>
            </select>
            
            <button
              onClick={handleGenerate}
              disabled={generating}
              className="inline-flex items-center px-4 py-2 border border-transparent text-sm font-medium rounded-md shadow-sm text-white bg-purple-600 hover:bg-purple-700 disabled:opacity-50"
            >
              {generating ? 'Generating...' : 'Generate Emails'}
            </button>
          </div>

          <div className="mt-6 grid gap-6 lg:grid-cols-3">
            {suggestions.map((suggestion, idx) => (
              <div key={idx} className="border rounded-lg p-4 flex flex-col hover:border-purple-300 transition-colors">
                <div className="flex-1">
                  <h4 className="font-semibold text-gray-900 mb-2 border-b pb-2">Variant {idx + 1}</h4>
                  <p className="text-sm font-medium text-gray-700 mb-1">Subject:</p>
                  <p className="text-sm text-gray-600 mb-3 bg-gray-50 p-2 rounded">{suggestion.subject}</p>
                  <p className="text-sm font-medium text-gray-700 mb-1">Body:</p>
                  <p className="text-sm text-gray-600 whitespace-pre-wrap bg-gray-50 p-2 rounded h-48 overflow-y-auto">
                    {suggestion.body}
                  </p>
                </div>
                <div className="mt-4 flex space-x-3 pt-4 border-t">
                  <button
                    onClick={() => handleSend(suggestion)}
                    disabled={sending === suggestion.variant_index}
                    className="flex-1 inline-flex justify-center items-center px-3 py-2 border border-transparent text-sm leading-4 font-medium rounded-md text-white bg-blue-600 hover:bg-blue-700 disabled:opacity-50"
                  >
                    <PaperAirplaneIcon className="h-4 w-4 mr-2" />
                    {sending === suggestion.variant_index ? 'Sending...' : 'Send'}
                  </button>
                  <button
                    onClick={() => copyToClipboard(`${suggestion.subject}\n\n${suggestion.body}`)}
                    className="inline-flex items-center p-2 border border-gray-300 shadow-sm text-sm font-medium rounded-md text-gray-700 bg-white hover:bg-gray-50"
                    title="Copy to clipboard"
                  >
                    <ClipboardDocumentIcon className="h-4 w-4" />
                  </button>
                </div>
              </div>
            ))}
            
            {suggestions.length === 0 && !generating && (
              <div className="col-span-3 text-center py-10 text-gray-500 bg-gray-50 rounded-lg border-2 border-dashed">
                No suggestions generated yet. Select a tone and click "Generate Emails" to start.
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
}