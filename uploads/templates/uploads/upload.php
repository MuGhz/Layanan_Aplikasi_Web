<?php
if(is_array($_FILES['uploader']['name']) && !empty($_FILES['uploader']['name'])){
        for($i=0;$i<sizeof($_FILES['uploader']['name']);$i++){
                move_uploaded_file($_FILES['uploader']['tmp_name'][$i], 'cache/'.$_FILES['uploader']['name'][$i]);
                echo "File ".$_FILES['uploader']['name'][$i]." uploaded successfully.<br>";
        }
}
?>
