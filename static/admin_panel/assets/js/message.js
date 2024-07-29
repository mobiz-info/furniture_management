let wsProtocol = 'ws://'
if (window.location.protocol == 'https:') {
    wsProtocol = 'wss://'
}
console.log(wsProtocol)
console.log(window.location.host)

const session_id = $("#instanceId").val();
const chatSocket = new WebSocket(
    wsProtocol
    + window.location.host
    + '/ws/comment_updates/'
    + session_id
    + '/'
);

// Function to append a new comment to the chat interface
function appendComment(comment) {
    const chatDetail = document.querySelector('.chat-detail');
    const newComment = `
        <div class="media">
            <div class="media-img">
                <img src="assets/images/users/user-{{ comment.user.id }}.jpg" alt="user" class="rounded-circle thumb-md">
            </div>
            <div class="media-body">
                <div class="chat-msg">
                    <p>${comment.content}</p>
                </div>
                <div class="chat-time">${comment.created_at}</div>
            </div><!--end media-body--> 
        </div><!--end media-->  
    `;
    chatDetail.innerHTML += newComment;
}

chatSocket.onmessage = function(e) {
    const data = JSON.parse(e.data);
    const comment = data['comment'];
    appendComment(comment);
};

document.getElementById('commentForm').addEventListener('submit', function(event) {
    event.preventDefault();
    const commentInput = document.querySelector('input[name="comment"]');
    const comment = commentInput.value;
    chatSocket.send(JSON.stringify({
        'comment': comment
    }));
    commentInput.value = '';
});