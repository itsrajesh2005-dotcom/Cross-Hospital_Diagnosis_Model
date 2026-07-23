import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import { Sidebar } from './components/layout/Sidebar';
import { Navbar } from './components/layout/Navbar';
import { DashboardPage } from './pages/DashboardPage';
import { HospitalsPage } from './pages/HospitalsPage';
import { RoundsPage } from './pages/RoundsPage';
import { ModelsPage } from './pages/ModelsPage';
import { AuditPage } from './pages/AuditPage';
import { ReportsPage } from './pages/ReportsPage';

export const App: React.FC = () => {
  return (
    <Router>
      <div className="flex min-h-screen bg-[#0b1329] text-slate-100">
        <Sidebar />
        <div className="flex-1 flex flex-col min-w-0">
          <Navbar />
          <main className="p-6 flex-1 overflow-y-auto">
            <Routes>
              <Route path="/" element={<DashboardPage />} />
              <Route path="/hospitals" element={<HospitalsPage />} />
              <Route path="/rounds" element={<RoundsPage />} />
              <Route path="/models" element={<ModelsPage />} />
              <Route path="/audit" element={<AuditPage />} />
              <Route path="/reports" element={<ReportsPage />} />
            </Routes>
          </main>
        </div>
      </div>
    </Router>
  );
};

export default App;
