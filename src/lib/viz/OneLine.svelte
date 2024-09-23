<script>
    export let color, width, height;

    const radius = 10;
    const rect = {
        w: 100,
        h: 10
    }
</script>


<svg {width} {height} viewBox="0 0 {width} {height}" preserveAspectRatio="xMinYMin">
        <g>
            <rect
                x={ radius/2 }
                y={ radius }
                width={ rect.w }
                height={ rect.h }
                stroke={ color } 
                fill={ color } />

            <circle 
                cx={ radius } 
                cy={ radius } 
                r={ radius } 
                fill={color} />
            
            <circle 
                cx={ radius } 
                cy={ radius } 
                r={ radius/2 } 
                fill="white" />
        </g>
</svg>
