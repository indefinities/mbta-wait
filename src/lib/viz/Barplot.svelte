<script>
  import * as d3 from "d3";
  export let color, data, width, height;

  const dataCopy = data.slice();

  dataCopy.shift();
  dataCopy.pop();

  $: xScale = d3.scaleLinear()
    .domain([0, d3.max(data, (d) => d.avg_wait_time)])
    .range([0, width]);

  $: yScale = d3.scaleBand()
    .domain(data)
    .range([10, height])
    .padding(0.15);

  $: heatScale = d3.scaleLinear()
    .domain([0, d3.max(data, (d) => d.avg_wait_time)])
    .range([0, 1]);

  function getDuration(seconds) {
    const mins = Math.floor(seconds / 60);
    return seconds > 60 ? `${ mins } minute${ mins > 1 ? 's' : '' }, ${ seconds % 60 } seconds` : `${ seconds } secs`
  }
</script>

<svg {width} {height} viewBox="0 0 {width} {height}" preserveAspectRatio="xMinYMin">
    {#each dataCopy as d}
    <g>
      <rect
          x={ xScale(0) }
          y={ yScale(d) }
          width={ xScale(d.avg_wait_time) }
          height={ yScale.bandwidth() }
          fill={ color } 
          fill-opacity={ heatScale(d.avg_wait_time) } />
      
      <text
        fill={ heatScale(d.avg_wait_time) < 0.5 ? color : 'white' } 
        text-anchor="end"
        x={ xScale(d.avg_wait_time) }
        y={ yScale(d) + yScale.bandwidth() / 2 }
        dx={-4}
        dy="0.35em">
          { getDuration(d.avg_wait_time) }
      </text>
    </g>
    {/each}
</svg>
