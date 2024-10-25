% Function returns the ID for the sound card "USB HQ AUDIO Mini adapter"
% Usage: 
% [ID_input, ID_output] = GetAudioID_4_USB_HQ
% If the adapter is not detected, it returns -1.
function [ID_input, ID_output] = GetAudioID_4_USB_HQ 
    
    ID_input= -1; ID_output = -1;
    audio_inputs = [
        "Mic USB HQ (USB Advanced Audio Device) (Windows DirectSound)", %#ok<COMNL>
        "Mikrofon (2 - USB Advanced Audio Device) (Windows DirectSound)", %#ok<COMNL>
        "USB AUDIO DEVICE: Audio (hw:1,0) (ALSA)"
    ];
    audio_outputs = [
        "Rep USB HQ (USB Advanced Audio Device) (Windows DirectSound)",
        "Reproduktory (2 - USB Advanced Audio Device) (Windows DirectSound)",
        "USB AUDIO DEVICE: Audio (hw:1,0) (ALSA)"
    ];

    info = audiodevinfo;

    disp("INPUTS...");
    for input = info.input
        disp(input);
        for input_name = audio_inputs
            disp("Checking input_name: " + input_name);
            if input.Name == input_name
                ID_input=input.ID;
                disp("Input found: " + input_name);
                break;
            end
        end
    end

    disp("OUTPUTS...");
    for output = info.output
        disp(output);
        for output_name = audio_outputs
            disp("Checking output_name: " + output_name);
            if output.Name == output_name
                ID_output=output.ID;
                disp("Output found: " + output_name);
                break;
            end
        end
    end
end
