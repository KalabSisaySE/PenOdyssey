const user = {
    first_name: 'John',
    last_name: 'Doe',
    bio: 'I\'m a software engineer with over 5 years of experience',
    interests: ['programming', 'reading', 'travelling'],
    liked_blogs: ['blog post 1', 'blog post 2', 'blog post 3'],
    written_blogs: ['blog post 4', 'blog post 5'],
    bookmarks: ['bookmark 1', 'bookmark 2', 'bookmark 3'],
    comments: ['comment 1', 'comment 2', 'comment 3']
};

const fullName = `${user.first_name} ${user.last_name}`;
const bio = user.bio;

document.getElementById('full-name').textContent = fullName;
document.getElementById('bio').textContent = bio;

const interestsList = user.interests.map((interest) => `<li>${interest}</li>`).join('');
document.getElementById('interests').innerHTML = interestsList;

const likedBlogsList = user.liked_blogs.map((blog) => `<li>${blog}</li>`).join('');
document.getElementById('liked-blogs').innerHTML = likedBlogsList;

const writtenBlogsList = user.written_blogs.map((blog) => `<li>${blog}</li>`).join('');
document.getElementById('written-blogs').innerHTML = writtenBlogsList;

const bookmarksList = user.bookmarks.map((bookmark) => `<li>${bookmark}</li>`).join('');
document.getElementById('bookmarks').innerHTML = bookmarksList;

const commentsList = user.comments.map((comment) => `<li>${comment}</li>`).join('');
document.getElementById('comments').innerHTML = commentsList;