<script>
      import * as d3 from "d3";
    export let data, width, height;

    $: xScale = d3.scaleLinear()
    .domain([0, d3.max(data)])
    .range([0, width]);

    $: yScale = d3.scaleBand()
    .domain(data)
    .range([0, height])
    .padding(0.1);
</script>


<svg {width} {height} viewBox="0 0 {width} {height}" preserveAspectRatio="xMinYMin">
    {#each data as d}
        <g>
            <text
            fill='black'
            text-anchor="end"
            x={ width }
            y={ yScale(d) + yScale.bandwidth() / 2 }
            dx={ -4 }
            dy="0.35em">
                {d}
            </text>
        </g>
    {/each}
</svg>
