from os import environ
from models.category import Category

if environ.get("STORAGE_TYPE") == "db":
    from storage.storage_factory import get_db_storage
    storage_engine = get_db_storage()
else:
    from storage.storage_factory import get_file_storage
    storage_engine = get_file_storage()


categories_data = {
    "Health and fitness": " This category is all about living a healthy lifestyle. It includes topics such as exercise, nutrition, and mental health.",
    "Travel and tourism": "This category is perfect for those who love to explore new places. It includes topics such as travel tips, destination reviews, and cultural experiences.",
    "Food and cooking": "This category is for foodies who love to cook and eat. It includes topics such as recipes, cooking techniques, and restaurant reviews.",
    "Technology and gadgets": "This category is for tech enthusiasts who love to stay up-to-date with the latest gadgets and trends. It includes topics such as product reviews, tech news, and how-to guides.",
    "Music and entertainment": "This category is perfect for those who love music and movies. It includes topics such as album reviews, movie reviews, and celebrity news.",
    "Fashion and beauty": "This category is for fashionistas who love to stay on top of the latest trends. It includes topics such as fashion tips, beauty product reviews, and makeup tutorials.",
    "Sports and athletics": "This category is for sports fans who love to follow their favorite teams and athletes. It includes topics such as game highlights, player profiles, and sports news.",
    "Business and finance": "This category is for entrepreneurs and business professionals who want to stay informed about the latest business news and trends. It includes topics such as finance tips, marketing strategies, and industry insights.",
    "Books and literature": "This category is for book lovers who want to discover new books and authors. It includes topics such as book reviews, author interviews, and literary news.",
    "Culture and society": "This category is for those who are interested in social issues and cultural trends. It includes topics such as diversity, equality, and social justice.",
    "Politics and government": "This category is for those who want to stay informed about the latest political news and events. It includes topics such as election coverage, policy analysis, and government news.",
    "Education and careers": "This category is for students and professionals who want to learn more about education and career opportunities. It includes topics such as job search tips, career advice, and educational resources.",
    "Home and family": "This category is for those who want to learn more about home improvement and family life. It includes topics such as home decor, DIY projects, and parenting advice.",
    "Environment and sustainability": "This category is for those who are passionate about the environment and want to learn more about sustainability. It includes topics such as climate change, renewable energy, and eco-friendly living.",
    "Art and design": "This category is for those who love art and design. It includes topics such as art history, design trends, and artist profiles.",
    "Lifestyle": "This category can include topics such as personal development, relationships, and self-care.",
    "History": "This category can include topics such as historical events, biographies, and cultural heritage.",
    "Science and nature": "This category can include topics such as space exploration, natural phenomena, and scientific discoveries.",
    "Humor": "This category can include topics such as jokes, memes, and funny videos."
}

# reload storage from file or db
storage_engine.reload()

# if no default categories are listed in file or db create them
if not storage_engine.all(model=Category):
    for name, desc in categories_data.items():
        obj = Category()
        obj.category_name = name
        obj.category_description = desc
        obj.save()
        storage_engine.reload()
