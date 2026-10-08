import {
    LineChart,
    Line,
    XAxis,
    YAxis,
    CartesianGrid,
    Tooltip,
    Legend,
    ResponsiveContainer
} from "recharts";


function PerformanceChart({ metrics }) {

    const chartData = [...metrics]
        .reverse()
        .map((metric) => ({

            time: new Date(
                metric.timestamp
            ).toLocaleTimeString(),

            cpu: metric.cpu_usage,

            memory: metric.memory_usage,

            disk: metric.disk_usage

        }));


    return (

        <ResponsiveContainer
            width="100%"
            height={350}
        >

            <LineChart data={chartData}>

                <CartesianGrid
                    strokeDasharray="3 3"
                />

                <XAxis
                    dataKey="time"
                />

                <YAxis
                    domain={[0, 100]}
                />

                <Tooltip />

                <Legend />

                <Line
                    type="monotone"
                    dataKey="cpu"
                    name="CPU %"
                />

                <Line
                    type="monotone"
                    dataKey="memory"
                    name="Memory %"
                />

                <Line
                    type="monotone"
                    dataKey="disk"
                    name="Disk %"
                />

            </LineChart>

        </ResponsiveContainer>

    );

}


export default PerformanceChart;