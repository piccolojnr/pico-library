$(document).ready(function () {

  for (const li of $("#book-info-list").children()) {
    $(li).find(".li-info-toggle").on("click", function () {
      $(li).toggleClass("closed");
      $(li).toggleClass("opened");
    })
  }

  for (const li of $("#bookmark-select-menu").children()) {
    $(li).find(".btn").on("click", function () {
      if ($(this).attr("data-value") === "remove")
        handleRemoveBookFromBookmark()
      else
        handleAddBookToBookmark($(this).attr("data-value"))
    })

  }
  if ($("#bookmarked").val()) {
    $("#bookmark-select-btn").on("click", handleRemoveBookFromBookmark)
  }
  // Event Handlers
  $("#nav-reviews-tab").on("click", handleReviewsTabClick);
  $("#nav-comments-tab").on("click", handleCommentsTabClick);
  $("#review-form").on("submit", handleReviewFormSubmit);
  $("#comment-form").on("submit", handleCommentFormSubmit);
  $("#load-more-comments-btn").on("click", handleLoadMoreCommentsClick);
  $("#load-more-reviews-btn").on("click", handleLoadMoreReviewsClick);
  // $("#add-bookmark-btn").on("click", handleAddBookToBookmark)

  // Initial Load of Comments and Reviews
  loadInitialCommentsAndReviews();
});
function handleReviewsTabClick() {
  handleTabClick($("#nav-reviews-tab"), $("#nav-comments-tab"), $("#reviews"), $("#comments"));
}

function handleCommentsTabClick() {
  handleTabClick($("#nav-comments-tab"), $("#nav-reviews-tab"), $("#comments"), $("#reviews"));
}

function handleReviewFormSubmit(event) {
  event.preventDefault();
  const reviewValues = getFormValues($("#review-form"));
  createComment(reviewValues.content, null, "review", null, parseFloat(reviewValues.rating));
}

function handleCommentFormSubmit(event) {
  event.preventDefault();
  const commentValues = getFormValues($("#comment-form"));
  createComment(commentValues.content, null, "comment", null);
}

function handleLoadMoreCommentsClick() {
  loadMoreComments();
}
function handleLoadMoreReviewsClick() {
  LoadMoreReviews()
}

function handleAddBookToBookmark(status) {
  $.ajax({
    url: "/api/v1/bookmarks/",
    method: 'POST',
    headers: {
      'Authorization': 'Bearer ' + $("#auth_token").val(),
      'Content-Type': 'application/json'
    },
    data: JSON.stringify({
      "book_id": $("#book_id").val(),
      "status": status
    })
    ,
    success: function (data) {
      $("#bookmark-select-btn").empty()
      $("#bookmark-select-btn").append($("<i>").addClass('fas fa-trash'))
      $("#bookmark-select-btn").attr("data-value", "remove")
      $("#bookmark-select-btn").removeClass("dropdown-toggle");
      $("#bookmark-select-btn").on("click", handleRemoveBookFromBookmark)
    },
    error: function (err) {
      console.log(err.responseJSON);
    }
  });
}
function handleRemoveBookFromBookmark() {
  $.ajax({
    url: "/api/v1/bookmarks/" + $("#book_id").val(),
    method: 'DELETE',
    headers: {
      'Authorization': 'Bearer ' + $("#auth_token").val(),
      'Content-Type': 'application/json'
    },
    success: function (data) {
      $("#bookmark-select-btn").empty()
      $("#bookmark-select-btn").append($("<i>").addClass('fas fa-bookmark'))
      $("#bookmark-select-btn").addClass("dropdown-toggle");
      $("#bookmark-select-btn").attr("data-value", "add")

    },
    error: function (err) {
      console.log(err.responseJSON);
    }
  });
}
// Tab click handler
function handleTabClick(clickedTab, otherTab, activeContent, inactiveContent) {
  const current = clickedTab.attr("aria-current");
  if (!current) {
    clickedTab.attr("aria-current", "page").addClass("active");
    otherTab.removeAttr("aria-current").removeClass("active");
    activeContent.addClass("active show");
    inactiveContent.removeClass("active show");
  }
}

//  handle votes
function handleVoteComment(comment_id, vote_type, d, u) {
  $.ajax({
    url: "/api/v1/comments/vote/" + comment_id,
    method: 'POST',
    headers: {
      'Authorization': 'Bearer ' + $("#auth_token").val(),
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

// Function to get form values
function getFormValues(form) {
  const values = {};
  form.find(":input").each(function () {
    if (this.name !== "") {
      values[this.name] = $(this).val();
    }
  });
  return values;
}


// Function to create comment
function createComment(content, parent_id, type = "comment", ele = null, rating = null) {
  let data = { 'book_id': parseInt($("#book_id").val()), "content": content, 'type': type };
  if (type === "reply") {
    data = { "content": content, "parent_id": parent_id, 'type': type };
  }
  if (type === "review") {
    data = { 'book_id': parseInt($("#book_id").val()), "content": content, "rating": rating, 'type': type }
  }
  $.ajax({
    url: "/api/v1/comments",
    headers: {
      'Authorization': 'Bearer ' + $("#auth_token").val(),
      'Content-Type': 'application/json'
    },
    method: 'POST',
    data: JSON.stringify(data),
    success: function (data) {
      let item = null;
      if (type === "review") {
        item = constructReview(data.item);
        if (ele === null) {
          ele = $("#reviews-list");
        }
      }
      else {
        item = constructComment(data.item);
        if (ele === null) {
          ele = $("#comments-list");
        }
      }
      ele.prepend(item);
    },
    error: function (err) {
      console.log(err.responseJSON);
    }
  });
}
// Function to load more comments
function loadMoreComments() {
  const el = $("#comments-list");
  const has_next = el.attr("data-has-next");
  if (has_next === "true") {
    const page = parseInt(el.attr("data-page")) + 1;
    getComments(null, "comment", null, page);
  }
}
// Function to load more reviews
function LoadMoreReviews() {
  const el = $("#reviews-list");
  const has_next = el.attr("data-has-next");
  if (has_next === "true") {
    const page = parseInt(el.attr("data-page")) + 1;
    getComments(null, "review", null, page);
  }
}
// Initial load of comments and reviews
function loadInitialCommentsAndReviews() {
  getComments(null, "review");
  getComments(null, "comment");
}

// Function to get comments
function getComments(parent_id = null, type = "comment", el = null, page = 1) {
  if (el === null) {
    if (type === "comment")
      el = $("#comments-list");
    else if (type === "review")
      el = $("#reviews-list");
  }

  let data = { "book_id": $("#book_id").val(), "type": type, "page": page };
  if (type === "reply") {
    data = { "parent_id": parent_id, "type": "reply", "page": page };
  }

  if (page === 1) {
    el.empty();
  }

  $.ajax({
    url: "/api/v1/comments",
    method: 'GET',
    data: data,
    success: function (data) {
      $("#comment-list-error-message").empty();

      el.attr("data-page", page);
      el.attr("data-has-next", data.has_next);

      displayComments(data.items, el, type);

      if (type === "comment") {
        if (data.has_next) {
          $("#load-more-comments-btn").css("display", "block");
        } else {
          $("#load-more-comments-btn").css("display", "none");
        }
      }
      else if (type === "review") {
        if (data.has_next) {
          $("#load-more-reviews-btn").css("display", "block");
        }
        else {
          $("#load-more-reviews-btn").css("display", "none");
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


// Function to display comments
function displayComments(input, el, type = "comment") {
  for (const comment of input) {
    if (type == "review") {
      el.append(constructReview(comment));
    } else {
      el.append(constructComment(comment));
    }
  }
}

function handleReply(content, parent_id, el) {
  createComment(content, parent_id, "reply", el);
}


function deleteComment(comment_id, el) {
  $.ajax({
    url: "/api/v1/comments/" + comment_id,
    method: 'DELETE',
    headers: {
      'Authorization': 'Bearer ' + auth_token,
      'Content-Type': 'application/json'
    },
    success: function (data) {
      $("#comment-list-error-message").empty();
      el.remove();
    },
    error: function (err) {
      console.log(err.responseJSON);
    }
  });
}


// Function to construct review HTML
function constructReview(review) {
  // Construct review HTML
  let reviewItem = $("<div>").addClass("reviewItem");
  let top = $("<div>").addClass("top");
  let bottom = $("<div>").addClass("bottom");

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


  if (review.user_profile.user.public_id === $("#user_public_id").val()) {
    let deleteBtn = $("<button>").addClass("btn").html(`<i class="fa-solid fa-trash text-danger"></i>`);
    deleteBtn.on("click", function () {
      deleteComment(review.id, reviewItem);
    });
    bottom.append(deleteBtn);
  }

  top.append(clientImage, rating);
  let article = $("<article>").addClass("review");
  let reviewText = $("<p>").text(review.content);
  let reviewDate = $("<p>").text(review.created_at);
  article.append(reviewText, reviewDate);
  reviewItem.append(top, article, bottom);
  return reviewItem;
}

// Function to construct comment HTML
function constructComment(comment) {
  // Construct comment HTML
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

  if ($("#auth_token").val()) {
    thumbsUpIcon.on("click", function () {
      handleVoteComment(comment.id, "upvote", downvoteNumBadge, upvoteNumBadge);
    })
    thumbsDownIcon.on("click", function () {
      handleVoteComment(comment.id, "downvote", downvoteNumBadge, upvoteNumBadge);
    });

    let replyForm = $("<form>").addClass("d-flex flex-row w-100").css("visibility", "hidden");
    let replyInput = $("<input>").attr("type", "text").addClass("form-control mr-3").attr("placeholder", "Add Reply").attr("name", "content").val("");
    let replySubmitBtn = $("<button>").addClass("btn btn-primary").attr("type", "submit").text("Reply");

    replyForm.on("submit", function (e) {
      e.preventDefault();
      handleReply(replyInput.val(), comment.id, repliesList);
      replyForm.css("visibility", "hidden");
    });

    replyForm.append(replyInput, replySubmitBtn);
    commentBox.append(replyForm);

    let replyBtn = $("<button>").addClass("btn").html(`<i class="fa-solid fa-reply"></i>`);
    replyBtn.on("click", function () {
      replyForm.css("visibility", replyForm.css("visibility") === "hidden" ? "visible" : "hidden");
    });
    commentFoot.append(replyBtn);

    if (comment.user_profile.user.public_id === $("#user_public_id").val()) {
      let deleteBtn = $("<button>").addClass("btn").html(`<i class="fa-solid fa-trash text-danger"></i>`);
      deleteBtn.on("click", function () {
        deleteComment(comment.id, commentItem);
      });
      commentFoot.append(deleteBtn);
    }
  }
  return commentItem;
}