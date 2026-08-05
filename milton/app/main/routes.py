import csv
import os
from datetime import datetime, timezone

from flask import render_template, session, redirect, request, jsonify
from app.main import main_bp

CONTACT_LOG_PATH = os.path.join(
    os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))),
    'contact_submissions.csv'
)

PRODUCTS_DB = [
    {
        'id': 1, 'brand': "L'ORÉAL PROFESSIONNEL", 'name': "Absolut Repair Molecular",
        'sub': "ინოვაციური მოლეკულური შამპუნი", 'price': "115.00",
        'image': "absolut-repair.mp4.mp4", 'is_video': True, 'collection': "absolut",
        'type': "shampoo", 'hair_type': "damaged", 'benefit': "repair",
        'desc': "პატენტური მოლეკულური ფორმულა, რომელიც აღადგენს თმის დაზიანებულ სტრუქტურას შიგნიდან.",
        'usage': "დაიტანეთ სველ თმაზე, ნაზად დაიმასაჟეთ კაფსულების ზონაში და კარგად ჩამოიბანეთ."
    },
    {
        'id': 2, 'brand': "L'ORÉAL PROFESSIONNEL", 'name': "Metal Detox Mask",
        'sub': "ღრმა წმენდისა და დაცვის ნიღაბი", 'price': "130.00",
        'image': "mask-3d.jpg", 'is_video': False, 'collection': "metal",
        'type': "mask", 'hair_type': "extended", 'benefit': "capsule",
        'desc': "ანტი-მეტალური დამცავი ტექნოლოგია. იცავს დაგრძელებულ თმას წყალში არსებული ლითონის ნაწილაკებისგან.",
        'usage': "შამპუნის შემდეგ თანაბრად გადაინაწილეთ თმის სიგრძეზე. გაიჩერეთ 5 წუთი."
    },
    {
        'id': 3, 'brand': "L'ORÉAL PROFESSIONNEL", 'name': "Metal Detox Oil",
        'sub': "კონცენტრირებული თერმოდამცავი ზეთი", 'price': "105.00",
        'image': "product-3.jpg", 'is_video': False, 'collection': "metal",
        'type': "oil", 'hair_type': "extended", 'benefit': "thermo",
        'desc': "მდიდრული ტექსტურის ზეთი, რომელიც უზრუნველყოფს 230°C-მდე საიმედო თერმოდაცვას.",
        'usage': "დაიტანეთ მცირე რაოდენობა ნესტიან ან მშრალ თმაზე სიგრძიდან ბოლოებისკენ."
    },
    {
        'id': 4, 'brand': "L'ORÉAL PROFESSIONNEL", 'name': "Scalp Advanced Treatment",
        'sub': "სკალპის ინტენსიური დამამშვიდებელი მკურნალობა", 'price': "95.00",
        'image': "photo_1_2026-06-17_18-00-43.jpg", 'is_video': False, 'collection': "scalp",
        'type': "mask", 'hair_type': "dry", 'benefit': "repair",
        'desc': "დერმატოლოგიურად სერტიფიცირებული ფორმულა ნიაცინამიდით. მომენტალურად ხსნის სკალპის ქავილს.",
        'usage': "სველ სკალპსა და თმაზე დაიტანეთ ნაზი წრიული მოძრაობებით. გაიჩერეთ 3-5 წუთი."
    },
    {
        'id': 5, 'brand': "L'ORÉAL PROFESSIONNEL", 'name': "Vitamino Color Shampoo",
        'sub': "შეღებილი თმის ფერის დამცავი შამპუნი", 'price': "85.00",
        'image': "photo_4_2026-06-17_18-00-43.jpg", 'is_video': False, 'collection': "vitamino",
        'type': "shampoo", 'hair_type': "colored", 'benefit': "thermo",
        'desc': "ძლიერი ანტიოქსიდანტური ფორმულა რესვერატროლით. იცავს შეღებილი თმის პიგმენტს გახუნებისგან.",
        'usage': "გადაინაწილეთ სველ თმაზე, კარგად ააფეთქეთ და ჩამოიბანეთ თბილი წყლით."
    }
]

@main_bp.route('/')
def index():
    return render_template('index.html')

@main_bp.route('/prices')
def prices():
    return render_template('prices.html')

@main_bp.route('/aftercare')
def aftercare():
    return render_template('aftercare.html')

@main_bp.route('/contact')
def contact():
    return render_template('contact.html')

@main_bp.route('/contact/submit', methods=['POST'])
def contact_submit():
    name = (request.form.get('name') or '').strip()
    phone = (request.form.get('phone') or '').strip()
    message = (request.form.get('message') or '').strip()

    if not name or not phone:
        return jsonify({'ok': False, 'error': 'missing_fields'}), 400

    row = [datetime.now(timezone.utc).isoformat(), name, phone, message]
    try:
        is_new = not os.path.exists(CONTACT_LOG_PATH)
        with open(CONTACT_LOG_PATH, 'a', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            if is_new:
                writer.writerow(['received_at', 'name', 'phone', 'message'])
            writer.writerow(row)
    except OSError:
        # ზოგიერთ hosting გარემოში (მაგ. serverless read-only filesystem) ჩაწერა
        # შეიძლება ვერ მოხერხდეს — მომხმარებელს მაინც ვუდასტურებთ მიღებას.
        pass

    return jsonify({'ok': True})

@main_bp.route('/shop')
def shop():
    return render_template('shop.html', products=PRODUCTS_DB)

@main_bp.route('/shop/product/<int:product_id>')
def product_detail(product_id):
    product = next((p for p in PRODUCTS_DB if p['id'] == product_id), None)
    related = [p for p in PRODUCTS_DB if p['id'] != product_id][:3]
    return render_template('product_detail.html', product=product, related=related)

@main_bp.route('/diagnostic', methods=['GET', 'POST'])
def diagnostic():
    product = None
    if request.method == 'POST':
        hair_type = request.form.get('hair_type')
        product = next((p for p in PRODUCTS_DB if p['hair_type'] == hair_type), None)
    return render_template('diagnostics.html', product=product)

@main_bp.route('/services')
def services():
    return render_template('services.html')

@main_bp.route('/extensions')
def extensions():
    return render_template('extensions.html')

@main_bp.route('/compare')
def compare():
    return render_template('compare.html')

@main_bp.route('/color-match')
def color_match():
    return render_template('color_match.html')

@main_bp.route('/academy')
def academy():
    return render_template('academy.html')

@main_bp.route('/academy/keratin')
def academy_keratin():
    return render_template('academy_keratin.html')

@main_bp.route('/lang/<lang_code>')
def set_lang(lang_code):
    if lang_code in ('ka', 'en'):
        session['lang'] = lang_code
    return redirect(request.referrer or '/')