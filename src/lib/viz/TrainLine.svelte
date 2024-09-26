<script>
    import * as d3 from "d3";
    export let color, data, width, height;

    const radius = 10;
    const rectWidth = 10;
    const dataCopy = data.slice();
    const endStops = [ dataCopy.shift(), dataCopy.pop()];

    $: yScale = d3.scaleBand()
        .domain(data)
        .range([radius, height])
        .padding(0.15);

    $: heatScale = d3.scaleLinear()
        .domain([0, d3.max(data, (d) => d.avg_wait_time)])
        .range([0, 1]);
</script>


<svg {width} {height} viewBox="0 0 {width} {height}" preserveAspectRatio="xMinYMin">
    <g>
    {#each dataCopy as d}
            <rect
                x={ width - 2*radius }
                y={ yScale(d) }
                width={ rectWidth }
                height={ yScale.bandwidth() }
                stroke={ color } 
                fill={ color } 
                fill-opacity={ heatScale(d.avg_wait_time) } />

            <!-- stop label -->
            <text
            fill='black'
            text-anchor="end"
            x={ width - rectWidth - radius - 10 }
            y={ yScale(d)}
            dx={ -4 }
            dy="0.35em">
                {d.stop_name}
            </text>

            <circle 
                cx={ width - 1.5*radius } 
                cy={ yScale(d) } 
                r={ radius } 
                fill={color} />
            
            <circle 
                cx={ width - 1.5*radius } 
                cy={ yScale(d) } 
                r={ radius/2 } 
                fill="white" />
    {/each}

    {#each endStops as d, i}
        {#if i < endStops.length - 1}
            <rect
                x={ width - 2*radius }
                y={ yScale(d) }
                width={ rectWidth }
                height={ yScale.bandwidth() }
                stroke={ color } 
                fill={ color } 
                fill-opacity={ heatScale(d.avg_wait_time) } />
        {/if}

            <!-- stop label -->
            <text
            fill='black'
            text-anchor="end"
            x={ width - rectWidth - radius - 10 }
            y={ yScale(d)}
            dx={ -4 }
            dy="0.35em">
                {d.stop_name}
            </text>

            <circle 
                cx={ width - 1.5*radius } 
                cy={ yScale(d) } 
                r={ radius } 
                fill={color} />
            
            <circle 
                cx={ width - 1.5*radius } 
                cy={ yScale(d) } 
                r={ radius/2 } 
                fill="white" />
    {/each}
    </g>
</svg>
