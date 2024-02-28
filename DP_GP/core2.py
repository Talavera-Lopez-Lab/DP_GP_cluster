def read_expression_data(data, true_times=False, unscaled=False, do_not_mean_center=False):
    def get_data_type(input_data):
        if os.path.isdir(input_data):
            return 'dir'
        elif os.path.isfile(input_data):
            return os.path.splitext(input_data)[1][1:]
        return ''
    
    def true_times_transformation(counts_df, true_times):
        counts_df = counts_df
        if true_times:
            t = np.array(counts_df.columns.tolist()).astype('float')
        else:
            # if not true_times, then create equally spaced time points
            t = np.array(range(counts_df.shape[1])).astype('float')
            np.vstack(np.nanmean(counts_df, axis=1))
        # transform gene expression as desired
        return t
    
    def array_transformation(gene_expression_array,
                             counts_df,
                             unscaled=unscaled, 
                             do_not_mean_center=do_not_mean_center):
        if unscaled == True and do_not_mean_center == True:
            pass
        elif unscaled == True and do_not_mean_center == False:
            gene_expression_array = gene_expression_array - np.vstack(np.nanmean(gene_expression_array, axis=1))
        elif unscaled == False and do_not_mean_center == True:
            mean = np.vstack(np.nanmean(gene_expression_array, axis=1))
            # first mean-center before scaling
            gene_expression_array = gene_expression_array - mean
            # scale
            std_dev = np.nanstd(counts_df, axis=1)
            valid_std_dev = std_dev != 0
            gene_expression_array[valid_std_dev] = gene_expression_array[valid_std_dev] / np.vstack(std_dev[valid_std_dev])
            # add mean once again, to disrupt mean-centering
            gene_expression_array = gene_expression_array + mean
        elif unscaled == False and do_not_mean_center == False:
            gene_expression_array = gene_expression_array - np.vstack(np.nanmean(gene_expression_array, axis=1))
            std_dev = np.nanstd(counts_df, axis=1)
            valid_std_dev = std_dev != 0
            gene_expression_array[valid_std_dev] = gene_expression_array[valid_std_dev] / np.vstack(std_dev[valid_std_dev])
        return gene_expression_array

            
    data_type = get_data_type(data)
    files = []
    gene_expression_array = None

    match data_type:
        case 'dir':
            files = os.listdir(data)
            files = [f for f in files if f.endswith('.txt') or f.endswith('.csv')]
            files_path = [os.path.join(data, file) for file in files]
            counts_df = pd.concat([pd.read_csv(file, sep='\t', index_col=0) for file in files_path], axis=0)
            counts_df = counts_df.groupby(counts_df.index).mean()
            gene_expression_array = np.array(counts_df)
            print("its a dir")
        case 'txt' | 'csv':
            counts_df = pd.read_csv(data, sep='\t', index_col=0)
            gene_expression_array = np.array(counts_df)
            print("its a text file")
        case 'h5ad':
            counts_df =(ad.read_h5ad(data)
                        .to_df()
                 .transpose())
            print('its an h5ad')
        case _ :
            print('invalid input')
    
    gene_expression_array = array_transformation(gene_expression_array, counts_df)
    gene_names = counts_df.index.tolist()
    t = true_times_transformation(counts_df=counts_df,
                                  true_times=true_times)
    t_labels = counts_df.columns.tolist()

    return(gene_expression_array, gene_names, t, t_labels)