$(document).ready(function () {

  $("#nav-reviews-tab").on("click", function () {
    handleTabClick($(this), $("#nav-comments-tab"), $("#reviews"), $("#comments"));
  });

  $("#nav-comments-tab").on("click", function () {
    handleTabClick($(this), $("#nav-reviews-tab"), $("#comments"), $("#reviews"));
  });
  $("#review-form").on("submit", function (e) {
    e.preventDefault();
    var $inputs = $('#review-form :input');
    const review_values = {}

    $inputs.each(function () {
      if (this.name !== "")
        review_values[this.name] = $(this).val();
    })

    console.log(review_values)
    createComment(review_values.content, null, "review", null, parseFloat(review_values.rating));

  })
  $("#comment-form").on("submit", function (e) {
    e.preventDefault();
    var $inputs = $('#comment-form :input');
    const comment_values = {}
    $inputs.each(function () {
      comment_values[this.name] = $(this).val();
    })
    createComment(comment_values.content, null, "comment", null);
  });


  $("#load-more-comments-btn").on("click", function () {
    const el = $("#comments-list")
    const has_next = el.attr("data-has-next")
    if (has_next === "true") {
      const page = parseInt(el.attr("data-page")) + 1
      getComments(null, "comment", null, page)
    }
  })

  const user_public_id = $("#user_public_id").val();
  const book_id = $("#book_id").val();
  const auth_token = $("#auth_token").val();
  function constructReview(review) {
    // <div class="reviewItem">
    //       <div class="top">
    //         <div class="clientImage">
    //           <img src="https://api.dicebear.com/8.x/bottts/svg?seed=" alt="" />
    //           <span>Raju Sheoran</span>
    //         </div>
    //         <ul>
    //           <li><i class="fa-solid fa-star"></i></li>
    //           <li><i class="fa-solid fa-star"></i></li>
    //           <li><i class="fa-solid fa-star"></i></li>
    //           <li><i class="fa-regular fa-star"></i></li>
    //           <li><i class="fa-regular fa-star"></i></li>
    //         </ul>
    //       </div>
    //       <article>
    //         <p class="review">
    //           Lorem ipsum dolor, sit amet consectetur adipisicing elit. Fugit
    //           beatae ipsa voluptatibus perferendis quos eaque nemo error tempora
    //           harum quas, laudantium tenetur, neque, facere exercitationem!
    //         </p>
    //         <p>Jan 01, 2023</p>
    //       </article>
    //     </div>
    let reviewItem = $("<div>").addClass("reviewItem");
    let top = $("<div>").addClass("top");
    let clientImage = $("<div>").addClass("clientImage");
    let avatarImg = $("<img>").attr("src", `https://api.dicebear.com/8.x/bottts/svg?seed=${review.user_profile.user.public_id}`).attr("alt", "");
    let clientName = $("<span>").text(`${review.user_profile.first_name} ${review.user_profile.last_name}`);
    clientImage.append(avatarImg, clientName);
    let rating = $("<ul>").addClass("rating");
    for (let i = 0; i < parseInt(review.rating); i++) {
      rating.append($("<li>").append($("<i>").addClass("fa-solid fa-star")));
    }
    for (let i = 0; i < 5 - parseInt(review.rating); i++) {
      rating.append($("<li>").append($("<i>").addClass("fa-regular fa-star")));
    }

    top.append(clientImage, rating);
    let article = $("<article>").addClass("review");
    let reviewText = $("<p>").text(review.content);
    let reviewDate = $("<p>").text(review.created_at);
    article.append(reviewText, reviewDate);
    reviewItem.append(top, article);
    return reviewItem;
  }
  function constructComment(comment) {
    let commentItem = $("<li>").addClass("comment-main-level");

    let commentAvatar = $("<div>").addClass("comment-avatar");
    let avatarImg = $("<img>").attr("src", `https://api.dicebear.com/8.x/bottts/svg?seed=${comment.user_profile.user.public_id}`).attr("alt", "");
    commentAvatar.append(avatarImg);

    let commentBox = $("<div>").addClass("comment-box");
    let commentHead = $("<div>").addClass("comment-head d-flex align-items-center justify-content-between");
    let commentHeadLeft = $("<div>").addClass("d-flex align-items-center gap-2");
    let commentName = $("<h6>").addClass("comment-name").html(`<a href="#">${comment.user_profile.first_name} ${comment.user_profile.last_name}</a>`);
    let commentTime = $("<span>").addClass("mb-2").text(comment.created_at);
    commentHeadLeft.append(commentName, commentTime);

    let commentHeadRight = $("<div>").addClass("d-flex align-items-center gap-2");

    let thumbsUpIcon = $("<button>").addClass("btn position-relative");
    thumbsUpIcon.css("padding", "0")
    thumbsUpIcon.append($("<i>").addClass("fa-solid fa-thumbs-up"));
    let upvoteNumBadge = $("<span>").addClass("position-absolute top-0 start-100 translate-middle badge rounded-pill text-danger fw-lighter").text(comment.upvotes);
    upvoteNumBadge.css("font-size", "10px");
    upvoteNumBadge.css("opacity", ".8");

    thumbsUpIcon.append(upvoteNumBadge);

    let thumbsDownIcon = $("<div>").addClass("btn position-relative");
    thumbsDownIcon.css("padding", "0")
    thumbsDownIcon.append($("<i>").addClass("fa-solid fa-thumbs-down"));
    let downvoteNumBadge = $("<span>").addClass("position-absolute top-0 start-100 translate-middle badge rounded-pill text-danger fw-lighter").text(comment.downvotes);
    downvoteNumBadge.css("font-size", "10px");
    downvoteNumBadge.css("opacity", ".8");
    thumbsDownIcon.append(downvoteNumBadge);


    let replyNum = $("<span>").addClass("reply-num").text(comment.number_of_replies);
    let repliesText = $("<span>").text("replies");
    commentHeadRight.append(thumbsUpIcon, thumbsDownIcon, replyNum, repliesText);

    commentHead.append(commentHeadLeft, commentHeadRight);

    let commentContent = $("<div>").addClass("comment-content").text(comment.content);
    let commentFoot = $("<div>").addClass("comment-foot d-flex align-items-center flex-row-reverse");

    commentBox.append(commentHead, commentContent, commentFoot);
    commentItem.append(commentAvatar, commentBox);

    let repliesList = $("<ul>").addClass("comments-list reply-list");
    commentItem.append(repliesList);

    if (comment.number_of_replies > 0) {
      let loadRepliesBtn = $("<button>").addClass("btn").text("Load Replies").css("font-size", "14px");
      loadRepliesBtn.attr("data-comment-id", comment.id);
      loadRepliesBtn.attr("data-open", "0");
      loadRepliesBtn.on("click", function () {
        if ($(this).attr("data-open") === "1") {
          repliesList.empty();
          $(this).attr("data-open", "0");
          $(this).text("Load Replies");
          return;
        }
        getComments(comment.id, "reply", repliesList);
        $(this).attr("data-open", "1");
        $(this).text("Hide Replies");
      });
      commentFoot.append(loadRepliesBtn);
    }

    if (auth_token) {
      thumbsUpIcon.on("click", function () {
        handleVoteComment(comment.id, "upvote", downvoteNumBadge, upvoteNumBadge);
      })
      thumbsDownIcon.on("click", function () {
        handleVoteComment(comment.id, "downvote", downvoteNumBadge, upvoteNumBadge);
      });

      let replyDiv = $("<div>").addClass("d-flex flex-row w-100").css("visibility", "hidden");
      let replyInput = $("<input>").attr("type", "text").addClass("form-control mr-3").attr("placeholder", "Add Reply").attr("name", "content").val("");
      let replySubmitBtn = $("<button>").addClass("btn btn-primary").text("Reply");

      replySubmitBtn.on("click", function () {
        handleReply(replyInput.val(), comment.id, repliesList);
        replyDiv.css("visibility", "hidden");
      });

      replyDiv.append(replyInput, replySubmitBtn);
      commentBox.append(replyDiv);

      let replyBtn = $("<button>").addClass("btn").html(`<i class="fa-solid fa-reply"></i>`);
      replyBtn.on("click", function () {
        replyDiv.css("visibility", replyDiv.css("visibility") === "hidden" ? "visible" : "hidden");
      });
      commentFoot.append(replyBtn);

      if (comment.user_profile.user.public_id === user_public_id) {
        let deleteBtn = $("<button>").addClass("btn").html(`<i class="fa-solid fa-trash text-danger"></i>`);
        deleteBtn.on("click", function () {
          deleteComment(comment.id);
        });
        commentFoot.append(deleteBtn);
      }
    }
    return commentItem;
  }

  function handleTabClick(clickedTab, otherTab, activeContent, inactiveContent) {
    var current = clickedTab.attr("aria-current");
    if (!current) {
      clickedTab.attr("aria-current", "page").addClass("active");
      otherTab.removeAttr("aria-current").removeClass("active");
      activeContent.addClass("active show");
      inactiveContent.removeClass("active show");
    }
  }


  function handleReply(content, parent_id, el) {
    createComment(content, parent_id, "reply", el);
  }

  function displayComment(input, el, type = "comment") {
    for (const c of input) {
      if (type == "review")
        el.append(constructReview(c));
      else
        el.append(constructComment(c));
    }
  }

  function handleVoteComment(comment_id, vote_type, d, u) {
    $.ajax({
      url: "/api/v1/comments/vote/" + comment_id,
      method: 'POST',
      headers: {
        'Authorization': 'Bearer ' + auth_token,
        'Content-Type': 'application/json'
      },
      data: JSON.stringify({ 'vote_type': vote_type }),
      success: function (data) {
        u.text(data.upvotes);
        d.text(data.downvotes);
      },
      error: function (err) {
        console.log(err.responseJSON);
      }
    });
  }

  function deleteComment(comment_id) {
    $.ajax({
      url: "/api/v1/comments/" + comment_id,
      method: 'DELETE',
      headers: {
        'Authorization': 'Bearer ' + auth_token,
        'Content-Type': 'application/json'
      },
      success: function (data) {
        $("#comment-list-error-message").empty();
        getComments();
      },
      error: function (err) {
        console.log(err.responseJSON);
      }
    });
  }

  function createComment(content, parent_id, type = "comment", ele = null, rating = null) {
    var data = { 'book_id': parseInt(book_id), "content": content, 'type': type };
    if (type === "reply") {
      data = { "content": content, "parent_id": parent_id, 'type': type };
    }
    if (type === "review") {
      data = { 'book_id': parseInt(book_id), "content": content, "rating": rating, 'type': type }
    }
    $.ajax({
      url: "/api/v1/comments",
      headers: {
        'Authorization': 'Bearer ' + auth_token,
        'Content-Type': 'application/json'
      },
      method: 'POST',
      data: JSON.stringify(data),
      success: function () {
        if (ele)
          getComments(parent_id, type, ele);
        else
          getComments(null, type);
      },
      error: function (err) {
        console.log(err.responseJSON);
      }
    });
  }

  function getComments(parent_id = null, type = "comment", el = null, page = 1) {
    if (el === null) {
      if (type === "comment")
        el = $("#comments-list")
      else if (type === "review")
        el = $("#reviews-list")
    }

    let data = { "book_id": book_id, "type": type, "page": page }
    if (type === "reply") {
      data = { "parent_id": parent_id, "type": "reply", "page": page }
    }

    if (page === 1) {
      el.empty()
    }

    $.ajax({
      url: "/api/v1/comments",
      method: 'GET',
      data: data,
      success: function (data) {
        $("#comment-list-error-message").empty();

        el.attr("data-page", page);
        el.attr("data-has-next", data.has_next)

        displayComment(data.items, el, type);

        if (type === "comment") {
          if (data.has_next) {
            $("#load-more-comments-btn").css("display", "block")
          }
          else {
            $("#load-more-comments-btn").css("display", "none")
          }
        }
      },
      error: function (err) {
        console.log(err.responseJSON);
        $("#comments-list").empty();
        $("#comments-list").html("No comments");
      }
    });
  }

  // Initial call to get comments
  getComments(null, "review");
  getComments(null, "comment");
});

