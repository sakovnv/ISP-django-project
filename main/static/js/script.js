window.onload = function () {
    window.setInterval(function () {
        let date = new Date()

        let hours = date.getHours()
        let minutes = date.getMinutes()
        let seconds = date.getSeconds()

        let day = date.getDay()

        if (hours < 10) hours = "0" + hours
        if (minutes < 10) minutes = "0" + minutes
        if (seconds < 10) seconds = "0" + seconds



        document.getElementById('time').textContent = hours + ":" + minutes + ":" + seconds
    })
}