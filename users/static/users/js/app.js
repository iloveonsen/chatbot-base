function previewImage() {
    var file = document.getElementById('id_profile_image').files[0];
    var reader = new FileReader();
    reader.onloadend = function() {
        document.getElementById('profile-image-preview').src = reader.result;
        document.getElementById('profile-image-preview').style.display = 'block';
    }
    if (file) {
        reader.readAsDataURL(file);
    } else {
        document.getElementById('profile-image-preview').src = "";
        document.getElementById('profile-image-preview').style.display = 'none';
    }
}