import ForceGraph3D from "react-force-graph-3d";
import { useMemo } from "react";

function GraphView3D({ data }) {

  const graphData = useMemo(() => {

    if (!data || !data.graph) return { nodes: [], links: [] };

    const suspiciousMap = {};

    data.suspicious_accounts.forEach(acc => {
      suspiciousMap[acc.account_id] = acc.suspicion_score;
    });

    return {

      nodes: data.graph.nodes.map(acc => ({
        id: acc,
        risk: suspiciousMap[acc] || 10
      })),

      links: data.graph.edges.map(e => ({
        source: e.source,
        target: e.target
      }))

    };

  }, [data]);

  if (!graphData.nodes.length) return null;

  return (
    <div style={{ height: "700px" }}>
      <ForceGraph3D
        graphData={graphData}

        nodeAutoColorBy="risk"

        nodeVal={node => node.risk / 10}

        nodeLabel={node =>
          `${node.id}\nRisk: ${node.risk}`
        }

        linkOpacity={0.3}

        enableNodeDrag={true}
      />
    </div>
  );
}

export default GraphView3D;
