<script>
  import * as d3 from "d3";

  export let color, data, width, height;

  $: xScale = d3.scaleLinear()
    .domain([0, d3.max(data)])
    .range([0, width]);

  $: yScale = d3.scaleBand()
    .domain(data)
    .range([0, height])
    .padding(0.15);

  $: heatScale = d3.scaleLinear()
    .domain([0, d3.max(data)])
    .range([0, 1]);

    function getDuration(seconds) {
      const mins = Math.floor(seconds / 60);
      return seconds > 60 ? `${ mins } minutes, ${ seconds % 60 } seconds` : `${ seconds } seconds`
    }

</script>

<svg {width} {height} viewBox="0 0 {width} {height}" preserveAspectRatio="xMinYMin">
    {#each data as d}
    <g>
      <rect
          x={ xScale(0) }
          y={ yScale(d) }
          width={ xScale(d) }
          height={ yScale.bandwidth() }
          fill={ color } 
          fill-opacity={ heatScale(d) } />
      
      <text
        fill={ heatScale(d) < 0.5 ? color : 'white' } 
        text-anchor="end"
        x={ xScale(d) }
        y={ yScale(d) + yScale.bandwidth() / 2 }
        dx={-4}
        dy="0.35em">
          { getDuration(d) }
      </text>
    </g>
    {/each}
</svg>
