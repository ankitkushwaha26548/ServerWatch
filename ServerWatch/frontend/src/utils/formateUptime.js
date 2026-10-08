export function formatUptime(totalSeconds) {

    const days = Math.floor(
        totalSeconds / 86400
    );

    totalSeconds %= 86400;


    const hours = Math.floor(
        totalSeconds / 3600
    );

    totalSeconds %= 3600;


    const minutes = Math.floor(
        totalSeconds / 60
    );


    return `${days} days, ${hours} hours, ${minutes} minutes`;
}