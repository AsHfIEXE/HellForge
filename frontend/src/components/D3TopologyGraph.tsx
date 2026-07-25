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
    if (!svgRef.current || !data.nodes.length) return;

    const width = svgRef.current.parentElement?.clientWidth || 800;
    const height = 500;

    d3.select(svgRef.current).selectAll('*').remove();

    const svg = d3
      .select(svgRef.current)
      .attr('width', width)
      .attr('height', height)
      .attr('viewBox', [0, 0, width, height]);

    const simulation = d3
      .forceSimulation(data.nodes)
      .force('link', d3.forceLink(data.links).id((d: any) => d.id).distance(100))
      .force('charge', d3.forceManyBody().strength(-300))
      .force('center', d3.forceCenter(width / 2, height / 2));

    const link = svg
      .append('g')
      .selectAll('line')
      .data(data.links)
      .join('line')
      .attr('stroke', 'rgba(0, 240, 255, 0.2)')
      .attr('stroke-width', 1.5);

    const node = svg
      .append('g')
      .selectAll('circle')
      .data(data.nodes)
      .join('circle')
      .attr('r', (d: any) => (d.group === 'root' ? 14 : 8))
      .attr('fill', (d: any) => {
        if (d.group === 'root') return '#9d4edd';
        if (d.risk > 70) return '#ff3b5c';
        if (d.risk > 40) return '#ff7b00';
        return '#00f0ff';
      })
      .attr('stroke', '#090c10')
      .attr('stroke-width', 2);

    node.append('title').text((d: any) => `${d.id} (Risk: ${d.risk})`);

    const text = svg
      .append('g')
      .selectAll('text')
      .data(data.nodes)
      .join('text')
      .text((d: any) => d.id)
      .attr('font-size', '10px')
      .attr('font-family', 'JetBrains Mono')
      .attr('fill', '#8b949e')
      .attr('dx', 12)
      .attr('dy', 4);

    simulation.on('tick', () => {
      link
        .attr('x1', (d: any) => d.source.x)
        .attr('y1', (d: any) => d.source.y)
        .attr('x2', (d: any) => d.target.x)
        .attr('y2', (d: any) => d.target.y);

      node.attr('cx', (d: any) => d.x).attr('cy', (d: any) => d.y);
      text.attr('x', (d: any) => d.x).attr('y', (d: any) => d.y);
    });

    return () => {
      simulation.stop();
    };
  }, [data]);

  return <svg ref={svgRef} style={{ width: '100%', height: '500px' }} />;
};
