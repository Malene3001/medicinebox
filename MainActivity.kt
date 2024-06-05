package com.example.medicinebox
import androidx.appcompat.app.AppCompatActivity
import android.os.Bundle
import android.os.Build
import android.widget.Button
import android.widget.Toast
import androidx.core.app.ActivityCompat
import org.json.JSONObject
import java.io.BufferedWriter
import java.io.OutputStreamWriter
import java.net.Socket
import android.Manifest
import android.widget.EditText
import java.net.InetSocketAddress

private val INTERNET_PERMISSION_CODE = 1001

val serverPort = 5000 // Server Port

fun createJsonPacket(of_off : String ): String {
    val jsonData = JSONObject()
    jsonData.put("status", "ok")
    jsonData.put("gpio", "$of_off")
    return jsonData.toString()
}

fun send_package(IP_adress :String, on_off : String) {
    Thread {
        val timeoutMillis = 1000 // Timeout in Millisec ( 1 second)
        val jsonPacket = createJsonPacket(on_off)

        val socket = Socket()

        try {
            val socketAddress = InetSocketAddress(IP_adress, serverPort)
            socket.connect(socketAddress, timeoutMillis)

            val writer = BufferedWriter(OutputStreamWriter(socket.getOutputStream()))
            writer.write(jsonPacket)
            writer.newLine()
            writer.flush()

            println("Send successfully: $jsonPacket")
        } catch (e: Exception) {
            println("Error during connect or transmission: ${e.message}")
        } finally {
            socket.close()
        }
    }.start()



}


class MainActivity : AppCompatActivity() {
    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        setContentView(R.layout.activity_main)
        val btn_on = findViewById<Button>(R.id.btn_on)
        val btn_off = findViewById<Button>(R.id.btn_off)
        val input_field = findViewById<EditText>(R.id.textIP)
        var ip_adress=""

        ip_adress = input_field.text.toString()


        if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.M) {
            ActivityCompat.requestPermissions(
                this,
                arrayOf(Manifest.permission.INTERNET),
                INTERNET_PERMISSION_CODE
            )
        }
        else
        {
            Toast.makeText(
                this@MainActivity,
                "Version don´t need special permission",
                Toast.LENGTH_LONG
            ).show()
        }


        btn_on.setOnClickListener{
            ip_adress = input_field.text.toString()
            Toast.makeText(
                this@MainActivity,
                "Turning On",
                Toast.LENGTH_LONG
            ).show()
            send_package("$ip_adress","on")
        }
        btn_off.setOnClickListener{
            ip_adress = input_field.text.toString()
            Toast.makeText(
                this@MainActivity,
                "Turning Off",
                Toast.LENGTH_LONG
            ).show()
            send_package("$ip_adress","off")
        }


    }
}