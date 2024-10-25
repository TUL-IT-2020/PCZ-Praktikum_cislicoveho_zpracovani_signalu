% Function returns the ID for the sound card "USB HQ AUDIO Mini adapter"
% Usage: 
% [ID_input, ID_output] = GetAudioID_4_USB_HQ
% If the adapter is not detected, it returns -1.
function [ID_input, ID_output] = GetAudioID_4_USB_HQ 
    info = audiodevinfo;
    N=length(info.input);
    disp("INPUTS...");
    ID_input= -1; ID_output = -1;
    for n=1:N
        disp(info.input(n));
        if info.input(n).Name == "Mic USB HQ (USB Advanced Audio Device) (Windows DirectSound)"
            ID_input=info.input(n).ID;
        end
        if info.input(n).Name == "Mikrofon (2 - USB Advanced Audio Device) (Windows DirectSound)"
            ID_input=info.input(n).ID;
        end
    end
    N=length(info.output);
    disp("OUTPUTS...");
    for n=1:N
        disp(info.output(n));
        if info.output(n).Name == "Rep USB HQ (USB Advanced Audio Device) (Windows DirectSound)"
            ID_output=info.output(n).ID;
        end
        if info.output(n).Name == "Reproduktory (2 - USB Advanced Audio Device) (Windows DirectSound)"
            ID_output=info.output(n).ID;
        end
    end
end
