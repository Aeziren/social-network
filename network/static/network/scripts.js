document.addEventListener("DOMContentLoaded", function() {
    const follow_btn = document.querySelector("#follow_btn")
    const edit_btn = document.querySelectorAll(".edit_btn")
    const hearts = document.querySelectorAll(".fa-heart")

    if (follow_btn) {
        follow_btn.addEventListener("click", function() {
            const from_user = follow_btn.dataset.from_user;
            const to_user = follow_btn.dataset.to_user;
            const follow_type = follow_btn.dataset.follow_type;
            follow_toggle(from_user, to_user, follow_type);
        })
    }

    if (edit_btn) {
        edit_btn.forEach(function (btn) {
            btn.addEventListener("click", function(event) {
                let post = event.target.parentNode;
                edit_post(post.dataset.id);
            })
        })
    }

    if (hearts) {
        hearts.forEach(function (heart_btn) {
            heart_btn.addEventListener("click", function(event) {
                post = event.target.parentNode
                toggle_like(post, event.target)
            })
        })
    }
})

function follow_toggle(from_user, to_user, follow_type) {
    fetch("/follow_toggle", {
        method: "POST",
        body: JSON.stringify({
            follow_type: follow_type,
            from_user: from_user,
            to_user: to_user,
        })
    })
    .then(function(response) {
        if (response.ok) {
            follow_btn = document.querySelector("#follow_btn");
            if (follow_type === "follow") {
                follow_btn.dataset.follow_type = "unfollow";
                follow_btn.textContent = "Unfollow";
            } else {
                follow_btn.dataset.follow_type = "follow";
                follow_btn.textContent = "Follow";
            }
        }
    })
}

function edit_post(post_id) {
    // Hide all edit buttons
    edit_btns = document.querySelectorAll(".edit_btn")
    edit_btns.forEach(function (btn) {
        btn.setAttribute("hidden", true);
    })

    // Get objects in the respective post
    const post = document.querySelector(`#post${post_id}`);
    const save_btn = post.querySelector(".save_btn");
    const cancel_btn = post.querySelector(".cancel_btn");
    let content_box = post.querySelector(".post_content");
    let text = content_box.textContent.trim();

    // Create text area with content
    content_box.innerHTML = `<textarea id="changes" style="width: 100%">${text}</textarea>`;

    // Add functionality to show and cancel buttons
    save_btn.addEventListener("click", function () {
        let changes = document.querySelector("#changes").value.trim();
        fetch(`/edit/${post_id}`, {
            method: "PUT",
            body: JSON.stringify({
                changes: changes
            })
        })
        .then(function (response) {
            if (response.ok) {
                hide();
                content_box.innerHTML = changes;
            } else {
                console.log(response)
            }
        })
    })
    cancel_btn.addEventListener("click", function () {
        hide();
        content_box.innerHTML = text;
    })

    function hide() {
        edit_btns.forEach(function (btn) {
            btn.removeAttribute("hidden");
        })

        save_btn.setAttribute("hidden", true);
        cancel_btn.setAttribute("hidden", true);
    }

    // Show hidden and cancel buttons
    save_btn.removeAttribute("hidden");
    cancel_btn.removeAttribute("hidden");
}

function toggle_like(post, button) {
    // Checks whether the action is like or unlike
    let action = button.dataset.action;
    // Get counter of likes
    const counter = post.querySelector(".qtt_likes")

    fetch(`/toggle_like/${post.dataset.id}`, {
        method: "POST",
        body: JSON.stringify({
            post_id: post.id,
            action: action
        })
    })
    .then(function (response) {
        if (response.ok) {
            if (action === "like"){
                counter.textContent = parseInt(counter.textContent) + 1;
                button.dataset.action = "unlike";
                button.style = "color: #ff3333"
            } else {
                counter.textContent = parseInt(counter.textContent) - 1;
                button.dataset.action = "like";
                button.style = "color: #686868"
            }
            button.classList.toggle("fa-regular");
            button.classList.toggle("fa-solid")
        }
    })
}
