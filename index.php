<?php
/*** KONFIGURATION ***/
$PAGE_TITLE = 'Feuerwehrhaus Gleidingen & Rethen';
$PAGE_LEAD = '';
$IMG_PATH = '';
$IMG_PREFIX = 'cam_';
$LINKS = array('https://www.fw-gleidingen.de/', 'http://www.fw-rethen.de/');
/*** KONFIGURATION ENDE ***/
?>

<head>
  <title><?php echo $PAGE_TITLE ?></title>
</head>

<?php
if ($IMG_PATH && substr($IMG_PATH, -1) != '/') $IMG_PATH .= '/';
$imgs = array_reverse(glob($IMG_PATH . $IMG_PREFIX . '*.[Jj][Pp][Gg]'));
$time_since = round((time() - filemtime($imgs[0])) / 60);
if ($time_since < 120)
  $time_since .= ' Minuten';
else
  $time_since = round($time_since / 60) . ' Stunden';
?>

<style>
* {
  margin: 0;
  padding: 0;
  font-family: sans-serif;
}

body {
  color: white;
  background-color: #343a40;
  font-size: 2.5vmin;
}

h1 {
  text-transform: uppercase;
  letter-spacing: 0.5vmin
  font-size: 5vmin;
}

.wrapper {
  /*! opacity: 0.65; */
  background-position: center;
  background-repeat: no-repeat;
  background-size: cover;
  background-image: url("<?php echo $imgs[0]; ?>");
  height: 100%;
}

.overlay {
  position: fixed;
  height: 100vh;
  width: 100vw;
}

.title {
  position: absolute;
  top: 1rem;
  left: 1rem;
  right: 1rem;
}

.links {
  position: absolute;
  bottom: 1rem;
  left: 1rem;
}

.footer {
  position: absolute;
  bottom: 1rem;
  right: 1rem;
}

.bg-red {
  display: inline-block;
  padding: 1vmin;
  background-color: #A20004;
  margin-bottom: 2vmin;
}

.btn {
  display: block;
  margin-top: 2vmin;
  padding: 2vmin 3vmin;
  border: 0.6vmin solid white;
  border-radius: 0.6vmin;
  background-color: unset;
  color: white;
  font-weight: bold;
  text-align: center;
  text-decoration: none;
  cursor: pointer;
}

.btn:hover {
  color: #343a40;
  background-color: white;
}
</style>

<body>
<div class="wrapper">

<div class="title">
  <?php if ($PAGE_TITLE): ?>
    <h1 class="bg-red"><?php echo $PAGE_TITLE; ?></h1>
  <?php endif; ?>
  <?php if ($PAGE_LEAD): ?>
    <h4 class="bg-red"><?php echo $PAGE_LEAD; ?></h4>
  <?php endif; ?>
</div>

<div class="links">
  <?php foreach ($LINKS as $link): ?>
    <a class="btn" href="<?php echo $link; ?>"><?php echo parse_url($link, PHP_URL_HOST); ?></a>
  <?php endforeach; ?>
</div>

<div class="footer">
  <h3>aktualisiert vor <?php echo $time_since; ?></h3>
</div>

</div>

</body>
