<script>
    export let color, width, height, endStops, totalTime;

    const radius = 15;
    const rect = {
        w: width,
        h: 10
    }

    function getDuration(seconds) {
        const mins = Math.floor(seconds / 60);
        return seconds > 60 ? `${ mins } minute${ mins > 1 ? 's' : '' }, ${ seconds % 60 } seconds` : `${ seconds } secs`
    }
</script>


<svg {width} {height} viewBox="0 0 {width} {height}" preserveAspectRatio="xMinYMin">
        <g>
            <rect
                x={ radius }
                y={ radius/2 + 3 }
                width={ rect.w }
                height={ rect.h }
                stroke={ color } 
                fill={ color } />

            {#each endStops as d, i}
                <text
                    fill='black'
                    text-anchor={ i > 0 ? 'end' : 'start'}
                    x={ i > 0 ? width : radius }
                    y={ height - 10 }
                    dx={ -4 }
                    dy="0.35em">
                        { d.stop_name }
                    </text>

                <circle 
                    cx={ i > 0 ? rect.w - radius : radius } 
                    cy={ radius } 
                    r={ radius } 
                    fill={ color } />
                
                <circle 
                    cx={ i > 0 ? rect.w - radius : radius } 
                    cy={ radius } 
                    r={ radius/2 } 
                    fill="white" />
            {/each}

            <text
                fill='black'
                text-anchor="middle"
                x={ width/2 }
                y={ height - 10 }
                dx={ -4 }
                dy="0.35em">
                The total average wait time for this trip was { getDuration(totalTime) }
            </text>
        </g>
</svg>
