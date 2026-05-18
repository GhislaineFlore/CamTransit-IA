package com.example.camtransit;

import android.os.Bundle;
import android.webkit.WebSettings;
import android.webkit.WebView;
import android.webkit.WebViewClient;
import androidx.appcompat.app.AppCompatActivity;

public class MainActivity extends AppCompatActivity {
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        WebView webView = findViewById(R.id.myWebView);
        WebSettings webSettings = webView.getSettings();
        
        webSettings.setJavaScriptEnabled(true); 
        webSettings.setDomStorageEnabled(true);   
        webSettings.setAllowFileAccess(true);     

        webView.setWebViewClient(new WebViewClient()); 

        // URL Provisoire locale
        webView.loadUrl("http://192.168.43.193:5000"); 
    }
}
