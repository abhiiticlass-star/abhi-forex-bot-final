let timer = null;
let running = false;

const countdownEl =
document.getElementById("countdown");

const signalEl =
document.getElementById("signal");

const confidenceEl =
document.getElementById("confidence");

const trendEl =
document.getElementById("trend");

const scoreEl =
document.getElementById("score");

const supportEl =
document.getElementById("support");

const resistanceEl =
document.getElementById("resistance");

const requestsEl =
document.getElementById("requests");

const reasonsEl =
document.getElementById("reasons");

const pairEl =
document.getElementById("pair");

const timeframeEl =
document.getElementById("timeframe");

const startBtn =
document.getElementById("startBtn");

const stopBtn =
document.getElementById("stopBtn");


function stopSoftware(){

    running = false;

    if(timer){
        clearInterval(timer);
        timer = null;
    }

    countdownEl.innerText = "STOPPED";
}


async function loadRequestStatus(){

    try{

        const res =
        await fetch("/api/requests");

        const data =
        await res.json();

        requestsEl.innerText =
        data.remaining;

    }catch(err){

        console.error(err);
    }
}


function getRemainingSeconds(){

    const now =
    new Date();

    const timeframe =
    timeframeEl.value;

    if(timeframe === "1min"){

        return 60 - now.getSeconds();
    }

    const minute =
    now.getMinutes();

    const second =
    now.getSeconds();

    const remainMinutes =
    5 - (minute % 5);

    let remain =
    remainMinutes * 60 - second;

    if(remain === 300){
        remain = 0;
    }

    return remain;
}


function formatTime(sec){

    const m =
    Math.floor(sec / 60);

    const s =
    sec % 60;

    return (
        String(m).padStart(2,"0")
        + ":"
        +
        String(s).padStart(2,"0")
    );
}


async function fetchSignal(){

    try{

        const pair =
        pairEl.value;

        const timeframe =
        timeframeEl.value;

        const res =
        await fetch(
            `/api/signal?pair=${pair}&timeframe=${timeframe}`
        );

        const data =
        await res.json();

        if(
            data.signal ===
            "DAILY LIMIT CROSSED"
        ){

            signalEl.className =
            "signal-box signal-stop";

            signalEl.innerText =
            "DAILY LIMIT CROSSED";

            requestsEl.innerText =
            "0";

            stopSoftware();

            return;
        }

        signalEl.className =
        "signal-box";

        if(data.signal === "CALL"){
            signalEl.classList.add(
                "signal-call"
            );
        }

        if(data.signal === "PUT"){
            signalEl.classList.add(
                "signal-put"
            );
        }

        if(data.signal === "AVOID"){
            signalEl.classList.add(
                "signal-avoid"
            );
        }

        signalEl.innerText =
        data.signal;

        confidenceEl.innerText =
        data.confidence + "%";

        trendEl.innerText =
        data.trend;

        scoreEl.innerText =
        data.score;

        supportEl.innerText =
        data.support ?? "-";

        resistanceEl.innerText =
        data.resistance ?? "-";

        requestsEl.innerText =
        data.remaining;

        reasonsEl.innerHTML = "";

        if(data.reasons){

            data.reasons.forEach(
                reason => {

                const li =
                document.createElement("li");

                li.innerText =
                reason;

                reasonsEl.appendChild(li);

            });
        }

    }catch(err){

        console.error(err);

        signalEl.innerText =
        "ERROR";
    }
}


function startCountdown(){

    if(running){
        return;
    }

    running = true;

    let remaining =
    getRemainingSeconds();

    countdownEl.innerText =
    formatTime(remaining);

    timer = setInterval(
        async () => {

        if(!running){
            return;
        }

        remaining--;

        if(remaining < 0){

            await fetchSignal();

            remaining =
            getRemainingSeconds();
        }

        countdownEl.innerText =
        formatTime(remaining);

    },1000);
}


startBtn.addEventListener(
    "click",
    () => {

    startCountdown();

});

stopBtn.addEventListener(
    "click",
    () => {

    stopSoftware();

});

loadRequestStatus();
