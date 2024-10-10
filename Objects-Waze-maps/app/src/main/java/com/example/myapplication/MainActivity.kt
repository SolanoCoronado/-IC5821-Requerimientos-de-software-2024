package com.example.myapplication
import android.Manifest
import android.app.AlertDialog
import android.content.pm.PackageManager
import android.graphics.Bitmap
import android.graphics.BitmapFactory
import android.os.Build
import android.os.Bundle
import android.util.Log
import android.widget.TextView
import android.widget.Toast
import androidx.activity.ComponentActivity
import androidx.annotation.OptIn
import androidx.annotation.RequiresApi
import androidx.camera.core.CameraSelector
import androidx.camera.core.ExperimentalGetImage
import androidx.camera.core.ImageAnalysis
import androidx.camera.core.ImageCapture
import androidx.camera.core.ImageProxy
import androidx.camera.lifecycle.ProcessCameraProvider
import androidx.camera.view.PreviewView
import androidx.core.app.ActivityCompat
import androidx.core.content.ContextCompat
import com.google.auth.oauth2.GoogleCredentials
import com.google.cloud.vision.v1.AnnotateImageRequest
import com.google.cloud.vision.v1.Image
import com.google.cloud.vision.v1.ImageAnnotatorClient
import com.google.cloud.vision.v1.ImageAnnotatorSettings
import com.google.cloud.vision.v1.Feature
import com.google.protobuf.ByteString
import java.io.ByteArrayOutputStream
import java.io.FileNotFoundException
import java.util.concurrent.ExecutorService
import java.util.concurrent.Executors
import java.util.Base64
import android.graphics.ImageFormat
import android.graphics.YuvImage
import android.graphics.Rect
import android.content.Intent
import android.net.Uri
import android.view.MenuItem
import android.widget.ImageView
import android.widget.PopupMenu
import android.view.View
import android.widget.EditText


class MainActivity : ComponentActivity() {
    private lateinit var cameraExecutor: ExecutorService
    private lateinit var imageAnnotatorClient: ImageAnnotatorClient
    private var cameraProvider: ProcessCameraProvider? = null

    @RequiresApi(Build.VERSION_CODES.O)
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_main)

        // Initialize the image annotator client and camera setup
        initializeImageAnnotatorClient()
        //setupCameraProvider()

        val menuButton: ImageView = findViewById(R.id.menuButton)
        menuButton.setOnClickListener {
            showPopupMenu(it)
        }
    }
    @RequiresApi(Build.VERSION_CODES.O)
    private fun showPopupMenu(view: View) {
        val popup = PopupMenu(this, view)
        popup.menuInflater.inflate(R.menu.menu_options, popup.menu)

        popup.setOnMenuItemClickListener { menuItem: MenuItem ->
            when (menuItem.itemId) {
                R.id.action_identifier -> {
                    // Identifier logic (already implemented)
                    requestPermission()
                    setupCameraProvider()
                    true
                }
                R.id.action_maps -> {
                    // Open Google Maps

                    true
                }
                // Submenú Coca Cola
                R.id.asetec_coca -> {
                    Toast.makeText(this, "Seleccionaste ASETEC en Coca Cola", Toast.LENGTH_SHORT).show()
                    try {
                        // Abrir Google Maps buscando la palabra ingresada
                        val searchQuery="ASETEC"
                        val mapsIntent = Intent(Intent.ACTION_VIEW, Uri.parse("geo:0,0?q=$searchQuery"))
                        mapsIntent.setPackage("com.google.android.apps.maps")
                        startActivity(mapsIntent)
                    } catch (e: Exception) {
                        // Manejar el caso donde Google Maps no está instalado
                        Toast.makeText(this, "Google Maps no está instalado", Toast.LENGTH_SHORT).show()
                    }
                    true
                }
                R.id.musi_coca -> {
                    Toast.makeText(this, "Seleccionaste Musi en Coca Cola", Toast.LENGTH_SHORT).show()

                    try {
                        // Abrir Google Maps buscando la palabra ingresada
                        val searchQuery="MUSI"
                        val mapsIntent = Intent(Intent.ACTION_VIEW, Uri.parse("geo:0,0?q=$searchQuery"))
                        mapsIntent.setPackage("com.google.android.apps.maps")
                        startActivity(mapsIntent)
                    } catch (e: Exception) {
                        // Manejar el caso donde Google Maps no está instalado
                        Toast.makeText(this, "Google Maps no está instalado", Toast.LENGTH_SHORT).show()
                    }
                    true
                }
                R.id.fresh_market_coca -> {
                    Toast.makeText(this, "Seleccionaste Fresh Market en Coca Cola", Toast.LENGTH_SHORT).show()
                    try {
                        // Abrir Google Maps buscando la palabra ingresada
                        val searchQuery="FreshMarket"
                        val mapsIntent = Intent(Intent.ACTION_VIEW, Uri.parse("geo:0,0?q=$searchQuery"))
                        mapsIntent.setPackage("com.google.android.apps.maps")
                        startActivity(mapsIntent)
                    } catch (e: Exception) {
                        // Manejar el caso donde Google Maps no está instalado
                        Toast.makeText(this, "Google Maps no está instalado", Toast.LENGTH_SHORT).show()
                    }
                    true
                }
                // Submenú Tropical
                R.id.asetec_tropical -> {
                    Toast.makeText(this, "Seleccionaste ASETEC en Tropical", Toast.LENGTH_SHORT).show()
                    try {
                        // Abrir Google Maps buscando la palabra ingresada
                        val searchQuery="ASETEC"
                        val mapsIntent = Intent(Intent.ACTION_VIEW, Uri.parse("geo:0,0?q=$searchQuery"))
                        mapsIntent.setPackage("com.google.android.apps.maps")
                        startActivity(mapsIntent)
                    } catch (e: Exception) {
                        // Manejar el caso donde Google Maps no está instalado
                        Toast.makeText(this, "Google Maps no está instalado", Toast.LENGTH_SHORT).show()
                    }
                    true
                }
                R.id.musi_tropical -> {
                    Toast.makeText(this, "Seleccionaste Musi en Tropical", Toast.LENGTH_SHORT).show()
                    try {
                        // Abrir Google Maps buscando la palabra ingresada
                        val searchQuery="MUSI"
                        val mapsIntent = Intent(Intent.ACTION_VIEW, Uri.parse("geo:0,0?q=$searchQuery"))
                        mapsIntent.setPackage("com.google.android.apps.maps")
                        startActivity(mapsIntent)
                    } catch (e: Exception) {
                        // Manejar el caso donde Google Maps no está instalado
                        Toast.makeText(this, "Google Maps no está instalado", Toast.LENGTH_SHORT).show()
                    }
                    true
                }
                R.id.fresh_market_tropical -> {
                    Toast.makeText(this, "Seleccionaste Fresh Market en Tropical", Toast.LENGTH_SHORT).show()
                    try {
                        // Abrir Google Maps buscando la palabra ingresada
                        val searchQuery="FreshMarket"
                        val mapsIntent = Intent(Intent.ACTION_VIEW, Uri.parse("geo:0,0?q=$searchQuery"))
                        mapsIntent.setPackage("com.google.android.apps.maps")
                        startActivity(mapsIntent)
                    } catch (e: Exception) {
                        // Manejar el caso donde Google Maps no está instalado
                        Toast.makeText(this, "Google Maps no está instalado", Toast.LENGTH_SHORT).show()
                    }
                    true
                }
                // Submenú Agua
                R.id.soda_comedor_agua -> {
                    Toast.makeText(this, "Seleccionaste Soda Comedor en Agua", Toast.LENGTH_SHORT).show()
                    try {
                        // Abrir Google Maps buscando la palabra ingresada
                        val searchQuery="Restaurante institucional tec"
                        val mapsIntent = Intent(Intent.ACTION_VIEW, Uri.parse("geo:0,0?q=$searchQuery"))
                        mapsIntent.setPackage("com.google.android.apps.maps")
                        startActivity(mapsIntent)
                    } catch (e: Exception) {
                        // Manejar el caso donde Google Maps no está instalado
                        Toast.makeText(this, "Google Maps no está instalado", Toast.LENGTH_SHORT).show()
                    }
                    true
                }
                R.id.soda_lago_agua -> {
                    Toast.makeText(this, "Seleccionaste Soda Lago en Agua", Toast.LENGTH_SHORT).show()
                    try {
                        // Abrir Google Maps buscando la palabra ingresada
                        val searchQuery="Soda El Lago"
                        val mapsIntent = Intent(Intent.ACTION_VIEW, Uri.parse("geo:0,0?q=$searchQuery"))
                        mapsIntent.setPackage("com.google.android.apps.maps")
                        startActivity(mapsIntent)
                    } catch (e: Exception) {
                        // Manejar el caso donde Google Maps no está instalado
                        Toast.makeText(this, "Google Maps no está instalado", Toast.LENGTH_SHORT).show()
                    }
                    true
                }
                R.id.soda_forestal_agua -> {
                    Toast.makeText(this, "Seleccionaste Soda Forestal en Agua", Toast.LENGTH_SHORT).show()
                    try {
                        // Abrir Google Maps buscando la palabra ingresada
                        val searchQuery="soda forestal"
                        val mapsIntent = Intent(Intent.ACTION_VIEW, Uri.parse("geo:0,0?q=$searchQuery"))
                        mapsIntent.setPackage("com.google.android.apps.maps")
                        startActivity(mapsIntent)
                    } catch (e: Exception) {
                        // Manejar el caso donde Google Maps no está instalado
                        Toast.makeText(this, "Google Maps no está instalado", Toast.LENGTH_SHORT).show()
                    }
                    true
                }
                R.id.asetec_agua -> {
                    Toast.makeText(this, "Seleccionaste ASETEC en Agua", Toast.LENGTH_SHORT).show()
                    try {
                        // Abrir Google Maps buscando la palabra ingresada
                        val searchQuery="ASETEC"
                        val mapsIntent = Intent(Intent.ACTION_VIEW, Uri.parse("geo:0,0?q=$searchQuery"))
                        mapsIntent.setPackage("com.google.android.apps.maps")
                        startActivity(mapsIntent)
                    } catch (e: Exception) {
                        // Manejar el caso donde Google Maps no está instalado
                        Toast.makeText(this, "Google Maps no está instalado", Toast.LENGTH_SHORT).show()
                    }
                    true
                }
                R.id.musi_agua -> {
                    Toast.makeText(this, "Seleccionaste Musi en Agua", Toast.LENGTH_SHORT).show()
                    try {
                        // Abrir Google Maps buscando la palabra ingresada
                        val searchQuery="musi"
                        val mapsIntent = Intent(Intent.ACTION_VIEW, Uri.parse("geo:0,0?q=$searchQuery"))
                        mapsIntent.setPackage("com.google.android.apps.maps")
                        startActivity(mapsIntent)
                    } catch (e: Exception) {
                        // Manejar el caso donde Google Maps no está instalado
                        Toast.makeText(this, "Google Maps no está instalado", Toast.LENGTH_SHORT).show()
                    }
                    true
                }
                R.id.fresh_market_agua -> {
                    Toast.makeText(this, "Seleccionaste Fresh Market en Agua", Toast.LENGTH_SHORT).show()
                    try {
                        // Abrir Google Maps buscando la palabra ingresada
                        val searchQuery="Freshmarket"
                        val mapsIntent = Intent(Intent.ACTION_VIEW, Uri.parse("geo:0,0?q=$searchQuery"))
                        mapsIntent.setPackage("com.google.android.apps.maps")
                        startActivity(mapsIntent)
                    } catch (e: Exception) {
                        // Manejar el caso donde Google Maps no está instalado
                        Toast.makeText(this, "Google Maps no está instalado", Toast.LENGTH_SHORT).show()
                    }
                    true
                }
                R.id.action_waze -> {
                    // Crear un AlertDialog con un campo de texto y un botón
                    val builder = AlertDialog.Builder(this)
                    builder.setTitle("Buscar en Waze")

                    // Crear un EditText para que el usuario ingrese la palabra a buscar
                    val input = EditText(this)
                    input.hint = "Ingrese la palabra para buscar"
                    builder.setView(input)

                    // Botón para abrir Waze con la palabra ingresada
                    builder.setPositiveButton("Abrir Waze") { dialog, _ ->
                        val searchQuery = input.text.toString()
                        if (searchQuery.isNotEmpty()) {
                            try {
                                // Abrir Waze buscando la palabra ingresada
                                val wazeIntent = Intent(Intent.ACTION_VIEW, Uri.parse("waze://?q=$searchQuery"))
                                startActivity(wazeIntent)
                            } catch (e: Exception) {
                                // Manejar el caso donde Waze no está instalado
                                Toast.makeText(this, "Waze app not found", Toast.LENGTH_SHORT).show()
                            }
                        } else {
                            Toast.makeText(this, "Debe ingresar una palabra", Toast.LENGTH_SHORT).show()
                        }
                        dialog.dismiss()
                    }

                    // Botón para cancelar la acción
                    builder.setNegativeButton("Cancelar") { dialog, _ -> dialog.cancel() }

                    // Mostrar el diálogo
                    builder.show()
                    true
                }

                else -> false
            }
        }
        popup.show()
    }


    @RequiresApi(Build.VERSION_CODES.O)
    private fun setupCameraProvider() {
        val cameraProviderFuture = ProcessCameraProvider.getInstance(this)
        cameraExecutor = Executors.newSingleThreadExecutor()
        cameraProviderFuture.addListener({
            try {
                cameraProvider = cameraProviderFuture.get()
                cameraProvider?.let { setupCamera(it, findViewById(R.id.previewView)) }
            } catch (exc: Exception) {
                Log.e("MainActivity", "Error initializing camera", exc)
            }
        }, ContextCompat.getMainExecutor(this))
    }

    private fun requestPermission() {
        if (ContextCompat.checkSelfPermission(this, Manifest.permission.CAMERA) == PackageManager.PERMISSION_GRANTED) {
            // Permiso concedido, no hace falta hacer nada
        } else {
            ActivityCompat.requestPermissions(this, arrayOf(Manifest.permission.CAMERA), 101)
        }
    }
    @RequiresApi(Build.VERSION_CODES.O)
    private fun setupCamera(cameraProvider: ProcessCameraProvider, previewView: PreviewView) {
        val preview = androidx.camera.core.Preview.Builder().build().also {
            it.setSurfaceProvider(previewView.surfaceProvider)
        }
        val imageCapture = ImageCapture.Builder().build()
        val imageAnalyzer = ImageAnalysis.Builder()
            .build()
            .also {
                it.setAnalyzer(cameraExecutor) { imageProxy ->
                    processImageProxy(imageProxy)
                }
            }
        val cameraSelector = CameraSelector.DEFAULT_BACK_CAMERA
        //val cameraSelector = CameraSelector.DEFAULT_FRONT_CAMERA
        try {
            cameraProvider.unbindAll()
            cameraProvider.bindToLifecycle(this, cameraSelector, preview, imageCapture, imageAnalyzer)
        } catch (exc: Exception) {
            Log.e("MainActivity", "Error al inicializar la cámara", exc)
            Toast.makeText(this, "Error al inicializar la cámara", Toast.LENGTH_SHORT).show()
        }
    }
    @RequiresApi(Build.VERSION_CODES.O)
    @OptIn(ExperimentalGetImage::class)
    private fun processImageProxy(imageProxy: ImageProxy) {
        val mediaImage = imageProxy.image
        mediaImage?.let {
            val planes = it.planes
            val yPlane = planes[0]
            val uPlane = planes[1]
            val vPlane = planes[2]
            val yBuffer = yPlane.buffer
            val uBuffer = uPlane.buffer
            val vBuffer = vPlane.buffer
            val ySize = yBuffer.remaining()
            val uSize = uBuffer.remaining()
            val vSize = vBuffer.remaining()
            val y = ByteArray(ySize)
            val u = ByteArray(uSize)
            val v = ByteArray(vSize)
            yBuffer.get(y)
            uBuffer.get(u)
            vBuffer.get(v)
            val yuvImage = YuvImage(y, ImageFormat.NV21, it.width, it.height, null)
            val outputStream = ByteArrayOutputStream()
            yuvImage.compressToJpeg(Rect(0, 0, it.width, it.height), 100, outputStream)
            val jpegData = outputStream.toByteArray()
            val bitmap = BitmapFactory.decodeByteArray(jpegData, 0, jpegData.size)
            if (bitmap == null) {
                Log.e("MainActivity", "Error al decodificar el byteArray en Bitmap.")
                runOnUiThread {
                    Toast.makeText(this, "Error al procesar la imagen", Toast.LENGTH_SHORT).show()
                }
                imageProxy.close()
                return
            }
            val resizedBitmap = Bitmap.createScaledBitmap(bitmap, 640, 480, true)
            val resizedOutputStream = ByteArrayOutputStream()
            resizedBitmap.compress(Bitmap.CompressFormat.JPEG, 85, resizedOutputStream)
            val resizedByteArray = resizedOutputStream.toByteArray()
            val image = Image.newBuilder()
                .setContent(ByteString.copyFrom(resizedByteArray))
                .build()
            val feature = Feature.newBuilder()
                .setType(Feature.Type.LABEL_DETECTION)
                .setMaxResults(5) // Mostrar hasta 5 etiquetas
                .build()
            val request = AnnotateImageRequest.newBuilder()
                .addFeatures(feature)
                .setImage(image)
                .build()
            try {
                val response = imageAnnotatorClient.batchAnnotateImages(listOf(request))
                Log.d("MainActivity", "Respuesta completa: ${response}")
                val labels = response.responsesList[0].labelAnnotationsList
                if (labels.isNotEmpty()) {
                    Log.d("MainActivity", "Labels encontrados: ${labels.map { it.description }}")
                    val textView = findViewById<TextView>(R.id.textView)
                    runOnUiThread {
                        textView.text = "Labels:\n"
                        for (label in labels) {
                            val description = label.description
                            val score = label.score
                            textView.text = "${textView.text}$description: ${"%.2f".format(score * 100)}%\n"
                        }
                    }
                } else {
                    Log.d("MainActivity", "No se encontraron etiquetas en la imagen.")
                    runOnUiThread {
                        val textView = findViewById<TextView>(R.id.textView)
                        textView.text = "No se encontraron etiquetas en la imagen."
                    }
                }
            } catch (e: Exception) {
                runOnUiThread {
                    Toast.makeText(this, "Error al procesar la imagen: ${e.message}", Toast.LENGTH_SHORT).show()
                }
            }
        }
        imageProxy.close()
    }
    private fun initializeImageAnnotatorClient() {
        try {
            val inputStream = resources.openRawResource(R.raw.credentials)
            val credentials = GoogleCredentials.fromStream(inputStream)
            Log.d("MainActivity", "Archivo de credenciales cargado correctamente")
            val settings = ImageAnnotatorSettings.newBuilder()
                .setCredentialsProvider { credentials }
                .build()
            imageAnnotatorClient = ImageAnnotatorClient.create(settings)
            Log.d("MainActivity", "Cliente de ImageAnnotator creado correctamente")
        } catch (e: FileNotFoundException) {
            Log.e("MainActivity", "Archivo de credenciales no encontrado", e)
            Toast.makeText(this, "Archivo de credenciales no encontrado", Toast.LENGTH_LONG).show()
        } catch (e: Exception) {
            Log.e("MainActivity", "Error al inicializar el cliente de Google Cloud Vision", e)
            Toast.makeText(this, "Error al inicializar el cliente de Google Cloud Vision: ${e.message}", Toast.LENGTH_LONG).show()
        }
    }
    override fun onRequestPermissionsResult(requestCode: Int, permissions: Array<out String>, grantResults: IntArray) {
        super.onRequestPermissionsResult(requestCode, permissions, grantResults)
        if (requestCode == 101) {
            if (grantResults.isNotEmpty() && grantResults[0] == PackageManager.PERMISSION_GRANTED) {
                // Permiso concedido, puedes continuar
            } else {
                Toast.makeText(this, "Permiso de cámara denegado", Toast.LENGTH_SHORT).show()
            }
        }
    }
    override fun onDestroy() {
        super.onDestroy()
        cameraProvider?.unbindAll()
        cameraExecutor.shutdown()
    }
}