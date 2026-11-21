async function runCPU(optimized) {

    const output = document.getElementById(
        optimized ? "cpu-after" : "cpu-before"
    );

    const endpoint = optimized
        ? "/profile/cpu/optimized"
        : "/profile/cpu";

    output.innerHTML = "Running profiler...";

    try {
        const response = await fetch(endpoint);
        const data = await response.json();

        output.innerHTML =
`Test: ${data.test}

Execution Time:
${data.execution_time_seconds} seconds

${optimized
    ? "Status: Optimized implementation"
    : "Bottleneck: " + data.bottleneck}

✓ Profiling completed`;

    } catch (error) {
        output.innerHTML = "Error running CPU profiling test.";
    }
}


async function runMemory(optimized) {

    const output = document.getElementById(
        optimized ? "memory-after" : "memory-before"
    );

    const endpoint = optimized
        ? "/profile/memory/optimized"
        : "/profile/memory";

    output.innerHTML = "Analyzing memory...";

    try {
        const response = await fetch(endpoint);
        const data = await response.json();

        output.innerHTML =
`Test: ${data.test}

Execution Time:
${data.execution_time_seconds} seconds

Peak Memory Usage:
${data.peak_memory_mb} MB

${optimized
    ? "Optimization: " + data.optimization
    : "Bottleneck: " + data.bottleneck}

✓ Peak memory profiling completed`;

    } catch (error) {
        output.innerHTML = "Error running memory profiling test.";
    }
}

async function runFullAnalysis() {

    const loading = document.getElementById("analysis-loading");

    loading.innerHTML =
        "Running 5 profiling iterations for each implementation...";

    try {

        const response = await fetch("/profile/cpu/compare");
        const data = await response.json();

        document.getElementById("slow-average").innerText =
            data.slow_average_seconds + " s";

        document.getElementById("optimized-average").innerText =
            data.optimized_average_seconds + " s";

        document.getElementById("cpu-improvement").innerText =
            data.improvement_percent + "%";

        document.getElementById("result-validation").innerText =
            data.same_result ? "✓ SAME" : "✕ DIFFERENT";

        document.getElementById("before-bar-value").innerText =
            data.slow_average_seconds + " s";

        document.getElementById("after-bar-value").innerText =
            data.optimized_average_seconds + " s";

        // Original execution time is the 100% reference.
        const optimizedWidth =
            (data.optimized_average_seconds /
             data.slow_average_seconds) * 100;

        document.getElementById("before-bar").style.width = "100%";

        document.getElementById("after-bar").style.width =
            optimizedWidth + "%";

        loading.innerHTML =
            `✓ Analysis completed using ${data.runs} runs per implementation.`;

    } catch (error) {

        loading.innerHTML =
            "Unable to complete performance analysis.";

    }
}