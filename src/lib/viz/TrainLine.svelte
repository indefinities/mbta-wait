<script>
    import * as d3 from "d3";
    export let color, data, width, height;

    const radius = 10;
    const rect = {
        w: 10,
        h: 20
    }

    $: yScale = d3.scaleBand()
    .domain(data)
    .range([0, height])
    .padding(0.25);

    $: heatScale = d3.scaleLinear()
    .domain([0, d3.max(data)])
    .range([0, 1]);
</script>


<svg {width} {height} viewBox="0 0 {width} {height}" preserveAspectRatio="xMinYMin">
    {#each data as d, i}
        <g>
            {#if i < data.length - 1}
                <rect
                    x={ radius/2 }
                    y={ yScale(d) }
                    width={ 10 }
                    height={ yScale.bandwidth() }
                    stroke={ color } 
                    fill={ color } 
                    fill-opacity={ heatScale(d) } />
            {/if}

            <circle 
                cx={ radius } 
                cy={ yScale(d) } 
                r={ radius } 
                fill={color} />
            
            <circle 
                cx={ radius } 
                cy={ yScale(d) } 
                r={ radius/2 } 
                fill="white" />
        </g>
    {/each}
</svg>
