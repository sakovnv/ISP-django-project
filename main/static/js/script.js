

window.onload = function () {
    window.setInterval(function () {
        let date = new Date()

        let hours = date.getHours()
        let minutes = date.getMinutes()
        let seconds = date.getSeconds()

        if (hours < 10) hours = "0" + hours
        if (minutes < 10) minutes = "0" + minutes
        if (seconds < 10) seconds = "0" + seconds

        document.getElementById('time').textContent = hours + ":" + minutes + ":" + seconds
    })
}

categorySubscribeList = document.querySelectorAll('[name=category-subscribe]')

Array.from(categorySubscribeList, function (e) {
    e.onclick = function () {

        let isSubscribed = e.classList.toggle('subscribed')
        let csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value
        $.ajax({
            headers: {'X-CSRFToken': csrftoken},
            url: 'subscribe_category/',
            type: 'POST',
            data: {
                'is_subscribed': isSubscribed,
                'category_id': e.getAttribute('value'),
            }
          });
        console.log(isSubscribed)
    }
})
