import { useRef } from 'react';
import gsap from 'gsap';
import { useGSAP } from '@gsap/react';

export default function DashboardIntro() {
  const container = useRef();

  useGSAP(() => {
    const tl = gsap.timeline();

    tl.from(".intro-text", {
      y: 50,
      opacity: 0,
      duration: 1,
      stagger: 0.2,
      ease: "power3.out"
    })
    .from(".intro-card", {
      scale: 0.8,
      opacity: 0,
      duration: 0.8,
      stagger: 0.1,
      ease: "back.out(1.7)"
    }, "-=0.5"); // Overlap previous animation by 0.5s

  }, { scope: container });

  return (
    <div ref={container} className="mb-8">
      <h1 className="intro-text text-3xl font-bold text-gray-900">
        Welcome back, <span className="text-indigo-600">User</span>
      </h1>
      <p className="intro-text text-gray-500 mt-2">
        Here is what's happening with your leads today.
      </p>
      
      {/* Example Stats Cards */}
      <div className="grid grid-cols-1 gap-5 sm:grid-cols-3 mt-6">
        {['Total Leads', 'Emails Sent', 'Response Rate'].map((item) => (
          <div key={item} className="intro-card bg-white overflow-hidden shadow rounded-lg px-4 py-5 sm:p-6 border border-gray-100 hover:shadow-lg transition-shadow">
             <dt className="text-sm font-medium text-gray-500 truncate">{item}</dt>
             <dd className="mt-1 text-3xl font-semibold text-gray-900">0</dd>
          </div>
        ))}
      </div>
    </div>
  );
}