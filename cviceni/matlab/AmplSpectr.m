%Funkce vykresli jednostranne amplitudove spektrum signalu x
%N je pocet vzorku
%Fs je vzorkovaci frekvence
function AmplSpectr(x, N,Fs)
    X=fft(x, N)./N;
    AX = 2*abs(X(1:N/2));
    AX(1)=AX(1)/2;
    NX=(0:Fs/N:Fs/2-1);
    stem(NX,AX );
end