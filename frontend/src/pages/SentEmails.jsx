import { useState, useEffect } from 'react';
import { emailsApi } from '../services/api';

export default function SentEmails() {
  const [emails, setEmails] = useState([]);

  useEffect(() => {
    emailsApi.getAllSentEmails()
      .then(res => setEmails(res.data))
      .catch(err => console.error(err));
  }, []);

  return (
    <div>
      <h1 className="text-xl font-semibold text-gray-900">Sent Emails</h1>
      <div className="mt-8 flex flex-col">
        <div className="-my-2 -mx-4 overflow-x-auto sm:-mx-6 lg:-mx-8">
          <div className="inline-block min-w-full py-2 align-middle md:px-6 lg:px-8">
            <div className="overflow-hidden shadow ring-1 ring-black ring-opacity-5 md:rounded-lg">
              <table className="min-w-full divide-y divide-gray-300">
                <thead className="bg-gray-50">
                  <tr>
                    <th className="py-3.5 pl-4 pr-3 text-left text-sm font-semibold text-gray-900">To</th>
                    <th className="px-3 py-3.5 text-left text-sm font-semibold text-gray-900">Subject</th>
                    <th className="px-3 py-3.5 text-left text-sm font-semibold text-gray-900">Date</th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-gray-200 bg-white">
                  {emails.map((email) => (
                    <tr key={email.id}>
                      <td className="whitespace-nowrap py-4 pl-4 pr-3 text-sm text-gray-900">{email.to_email}</td>
                      <td className="whitespace-nowrap px-3 py-4 text-sm text-gray-500">{email.subject}</td>
                      <td className="whitespace-nowrap px-3 py-4 text-sm text-gray-500">{new Date(email.sent_at).toLocaleDateString()}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}