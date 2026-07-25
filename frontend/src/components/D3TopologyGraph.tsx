import React, { useEffect, useRef } from 'react';
import * as d3 from 'd3';

interface GraphProps {
  data: {
    nodes: any[];
    links: any[];
  };
}

export const D3TopologyGraph: React.FC<GraphProps> = ({ data }) => {
  const svgRef = useRef<SVGSVGElement | null>(null);

  useEffect(() => {
    if (!svgRef.current) return;

    const width = svgRef.current.parentElement?.clientWidth || 800;
    const height = 450;

    d3.select(svgRef.current).selectAll('*').remove();

    if (!data.nodes.length) {
      const svgEmpty = d3
        .select(svgRef.current)
        .attr('width', width)
        .attr('height', height)
        .attr('viewBox', [0, 0, width, height]);

      svgEmpty
        .append('text')
        .attr('x', width / 2)
        .attr('y', height / 2)
        .attr('text-anchor', 'middle')
        .attr('fill', '#64748b')
        .attr('font-size', '13px')
        .attr('font-family', 'JetBrains Mono')
        .text('No active infrastructure nodes mapped. Run a target scan to render network topology.');

      return;
    }

    const svg = d3
      .select(svgRef.current)
      .attr('width', width)
      .attr('height', height)
      .attr('viewBox', [0, 0, width, height]);

    // Zoom & Pan behavior
    const container = svg.append('g');
    const zoom = d3.zoom<SVGSVGElement, unknown>().scaleExtent([0.5, 3]).on('zoom', (event) => {
      container.attr('transform', event.transform);
    });
    svg.call(zoom as any);

    // Deep clone nodes and links to prevent d3 mutation errors
    const nodes = data.nodes.map((n) => ({ ...n }));
    const links = data.links.map((l) => ({ ...l }));

    const simulation = d3
      .forceSimulation(nodes)
      .force('link', d3.forceLink(links).id((d: any) => d.id).distance(110))
      .force('charge', d3.forceManyBody().strength(-350))
      .force('center', d3.forceCenter(width / 2, height / 2))
      .force('collision', d3.forceCollide().radius(24));

    // Draw Links
    const link = container
      .append('g')
      .selectAll('line')
      .data(links)
      .join('line')
      .attr('stroke', '#232b3e')
      .attr('stroke-width', 1.5)
      .attr('stroke-dasharray', (d: any) => (d.type === 'inferred' ? '4,4' : '0'));

    // Draw Nodes
    const node = container
      .append('g')
      .selectAll('g')
      .data(nodes)
      .join('g')
      .style('cursor', 'pointer')
      .call(
        d3
          .drag<SVGGElement, any>()
          .on('start', (event, d) => {
            if (!event.active) simulation.alphaTarget(0.3).restart();
            d.fx = d.x;
            d.fy = d.y;
          })
          .on('drag', (event, d) => {
            d.fx = event.x;
            d.fy = event.y;
          })
          .on('end', (event, d) => {
            if (!event.active) simulation.alphaTarget(0);
            d.fx = null;
            d.fy = null;
          })
      );

    // Outer Circle Glow / Pulsing Ring for Critical Nodes
    node
      .append('circle')
      .attr('r', (d: any) => (d.group === 'root' ? 14 : d.risk > 60 ? 12 : 9))
      .attr('fill', (d: any) => {
        if (d.group === 'root') return 'rgba(59, 130, 246, 0.15)';
        if (d.risk > 60) return 'rgba(239, 68, 68, 0.15)';
        if (d.risk > 30) return 'rgba(249, 115, 22, 0.15)';
        return 'rgba(16, 185, 129, 0.15)';
      })
      .attr('stroke', (d: any) => {
        if (d.group === 'root') return '#3b82f6';
        if (d.risk > 60) return '#ef4444';
        if (d.risk > 30) return '#f97316';
        return '#10b981';
      })
      .attr('stroke-width', 1.5);

    // Inner Core Circle
    node
      .append('circle')
      .attr('r', (d: any) => (d.group === 'root' ? 7 : 4))
      .attr('fill', (d: any) => {
        if (d.group === 'root') return '#3b82f6';
        if (d.risk > 60) return '#ef4444';
        if (d.risk > 30) return '#f97316';
        return '#10b981';
      });

    // Node Labels
    node
      .append('text')
      .text((d: any) => d.id)
      .attr('font-size', '11px')
      .attr('font-family', 'JetBrains Mono')
      .attr('font-weight', (d: any) => (d.group === 'root' ? '700' : '400'))
      .attr('fill', (d: any) => (d.group === 'root' ? '#f8fafc' : '#94a3b8'))
      .attr('dx', 16)
      .attr('dy', 4);

    // Interactive Tooltip Title
    node.append('title').text((d: any) => `${d.id}\nGroup: ${d.group}\nRisk Score: ${d.risk}/100`);

    simulation.on('tick', () => {
      link
        .attr('x1', (d: any) => d.source.x)
        .attr('y1', (d: any) => d.source.y)
        .attr('x2', (d: any) => d.target.x)
        .attr('y2', (d: any) => d.target.y);

      node.attr('transform', (d: any) => `translate(${d.x},${d.y})`);
    });

    return () => {
      simulation.stop();
    };
  }, [data]);

  return <svg ref={svgRef} style={{ width: '100%', height: '450px', background: 'var(--bg-dark)', borderRadius: '6px' }} />;
};
