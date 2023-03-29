function MM = loadFile_h5(data_num, data_dir, dv_dir,write_dir)
    if nargin <3
        dv_dir = 'E:\Dropbox\Dropbox\vault\';
    end
    if nargin <4
        write_dir = dv_dir;
    end
    
    data_dir = [dv_dir data_dir '\'];
    
    start_dir = cd;
    cd(data_dir)
    datanames = ls([data_num '*']);
    
    if isempty(getmat(datanames))

       dataname=geth5(datanames);
       dataname
       ff=h5read(dataname,'/DataVault/');
       fields = fieldnames(ff);
       for i = 1:length(fields)
           MM(:,i) = ff.(fields{i});
       end
%        save([write_dir dataname(1:end-5) '.mat'],'MM')
  
    else
       o = load(getmat(datanames),'MM');
       MM = o.MM;
    end
    cd(start_dir)
    
   function h5file = geth5(fnames)
        h5file='';
        for i =1:size(fnames,1)
            if fnames(i,end-4:end) == '.hdf5'
                h5file = fnames(i,:);
            end
        end
   end 

   function matfile = getmat(fnames)
        matfile='';
        for i =1:size(fnames,1)
            if fnames(i,end-3:end) == '.mat'
                matfile = fnames(i,:);
            end
        end
   end
end