import './index.css';
import UploadSection from "./components/UploadSection";
import GraphView3D from "./components/GraphView3D";
import SuspiciousTable from "./components/SuspiciousTable";
import RingTable from "./components/RingTable";
import DownloadButton from "./components/DownloadButton";
import { useState } from "react";

function App() {

  const [data, setData] = useState(null);

  return (
    <>
      <div className="grid-bg" />
      <div className="orb orb-1" />
      <div className="orb orb-2" />
      <div className="orb orb-3" />

      <div className="app-wrapper">

        <header className="hero-header">
          <div className="hero-badge">
            <span className="dot" />
            AI-Powered Financial Intelligence
          </div>
          <h1 className="hero-title">
            Money Mule<br />Detection System
          </h1>
          <p className="hero-subtitle">
            Upload transaction data to detect fraud rings,
            suspicious transfers and money muling patterns.
          </p>
        </header>

        {data && data.summary && (
          <div className="stats-grid">

            <div className="stat-card blue">
              <div className="stat-label">Accounts</div>
              <div className="stat-value">
                {data.summary.total_accounts_analyzed}
              </div>
            </div>

            <div className="stat-card red">
              <div className="stat-label">Suspicious</div>
              <div className="stat-value">
                {data.summary.suspicious_accounts_flagged}
              </div>
            </div>

            <div className="stat-card orange">
              <div className="stat-label">Fraud Rings</div>
              <div className="stat-value">
                {data.summary.fraud_rings_detected}
              </div>
            </div>

            <div className="stat-card green">
              <div className="stat-label">Processing</div>
              <div className="stat-value">
                {data.summary.processing_time_seconds < 1
                  ? `${Math.round(data.summary.processing_time_seconds * 1000)}ms`
                  : `${data.summary.processing_time_seconds.toFixed(2)}s`}
              </div>
            </div>

          </div>
        )}

        <div className="upload-zone">
          <UploadSection setData={setData} hasData={!!data} />
        </div>

        {data && (
          <>
            <div className="divider" />

            {/* 🔥 FORCE GRAPH REMOUNT */}
            <GraphView3D key={JSON.stringify(data?.fraud_rings)} data={data} />

            <div className="divider" />
            <RingTable rings={data.fraud_rings} />

            <div className="divider" />
            <SuspiciousTable accounts={data.suspicious_accounts} />

            <div className="divider" />
            <DownloadButton json={data || {}} />
          </>
        )}

      </div>
    </>
  );
}

export default App;
