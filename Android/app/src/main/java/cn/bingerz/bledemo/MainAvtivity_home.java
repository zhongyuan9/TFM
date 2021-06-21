package cn.bingerz.bledemo;

import android.content.Intent;
import android.os.Bundle;
import android.view.View;
import android.widget.Button;
import android.support.v7.app.AppCompatActivity;

public class MainAvtivity_home extends AppCompatActivity implements View.OnClickListener {
    private Button btn_Mqtt, btn_Ble;
    private Intent intent;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_home);

        btn_Mqtt = findViewById(R.id.btn_Mqtt);
        btn_Ble = findViewById(R.id.btn_Ble);

        btn_Ble.setOnClickListener(this);
        btn_Mqtt.setOnClickListener(this);

    }
    public void onClick(View v) {
        switch (v.getId()){
            case R.id.btn_Mqtt:
                intent = new Intent(this, MainActivity_mqtt.class);
                break;
            case R.id.btn_Ble:
                intent = new Intent(this, MainActivity_ble.class);
                break;
        }
        if(intent!=null){
            startActivity(intent);
        }
    }

}
