import CytoscapeComponent from "react-cytoscapejs";
import { useEffect, useState } from "react";

function GraphView({ data }) {

  const [elements, setElements] = useState([]);
  const [key, setKey] = useState(0);

  useEffect(() => {

    if (!data || !data.fraud_rings) return;

    let newElements = [];
    let nodeSet = new Set();

    // 🔥 LIMIT GRAPH SIZE FOR LARGE DATASETS
    const MAX_NODES = 200;
    let count = 0;

    // ============================
    // CREATE NODES
    // ============================
    for (let ring of data.fraud_rings) {

      for (let acc of ring.member_accounts) {

        if (count > MAX_NODES) break;

        if (!nodeSet.has(acc)) {

          nodeSet.add(acc);
          count++;

          let scoreObj = data.suspicious_accounts.find(
            a => a.account_id === acc
          );

          newElements.push({
            data: {
              id: acc,
              label: acc,
              risk_score: scoreObj?.suspicion_score || 10
            }
          });

        }
      }
    }

    // ============================
    // CREATE STAR EDGES (NOT CHAIN)
    // ============================
    data.fraud_rings.forEach((ring) => {

      const members = ring.member_accounts;

      if (members.length > 1) {

        let center = members[0];

        for (let i = 1; i < members.length; i++) {

          if(nodeSet.has(members[i])){

            newElements.push({
              data: {
                id: `${center}-${members[i]}`,
                source: center,
                target: members[i]
              }
            });

          }
        }
      }

    });

    setElements(newElements);
    setKey(prev => prev + 1);

  }, [data]);

  if (!elements.length) return null;

  return (
    <div style={{ height: "600px", background: "#0b1220", borderRadius: "12px" }}>
      <CytoscapeComponent
        key={key}
        elements={elements}

        style={{ width: "100%", height: "100%" }}

        // ⚡ FAST LAYOUT (BANK SAFE)
        layout={{
          name: "breadthfirst",
          fit: true,
          padding: 30,
          animate: false
        }}

        
        minZoom={0.4}
        maxZoom={2}

        stylesheet={[
          {
            selector: "node",
            style: {
              label: "data(label)",
              width: 40,
              height: 40,
              "background-color": "#1e90ff",
              color: "#fff",
              "font-size": 12,
              "text-valign": "center",
              "text-halign": "center"
            }
          },
          {
            selector: "node[risk_score > 80]",
            style: {
              "background-color": "#ff3b3b"
            }
          },
          {
            selector: "node[risk_score > 60]",
            style: {
              "background-color": "#ff9800"
            }
          },
          {
            selector: "edge",
            style: {
              width: 2,
              "line-color": "#aaa",
              "curve-style": "haystack"
            }
          }
        ]}
      />
    </div>
  );
}

export default GraphView;
